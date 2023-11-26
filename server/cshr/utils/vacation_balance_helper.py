from typing import Dict, List
from server.cshr.models.users import User
from server.cshr.models.vacations import (
    REASON_CHOICES,
    OfficeVacationBalance,
    Vacation,
    VacationBalance,
)

import datetime
import os

from server.cshr.services.public_holidays import get_user_holidays


class StanderdVacationBalance:
    def __init__(self):
        self.abspath = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(f"{self.abspath}/vacation_balance.json")

    def check(self, user) -> VacationBalance:
        try:
            balance = VacationBalance.objects.get(user=user)
            for field in balance._meta.fields:
                actual_value: int = getattr(balance, field.name)
                if (
                    type(actual_value) == dict
                    and len(actual_value) > 0
                    and field.name != "actual_balance"
                ):
                    for k, v in actual_value.items():
                        balance_attr: int = getattr(balance, k)
                        if balance_attr + v < 100:
                            setattr(balance, k, balance_attr + v)
            return balance
        except VacationBalance.DoesNotExist:
            return self.create_new_balance(user)

    def create_new_balance_values(self, user: User) -> Dict:
        # this help to divide to get the total days based on joining date
        month: int = 12 - user.created_at.month
        balance = OfficeVacationBalance.objects.get(
            year=datetime.datetime.now().year, location=user.location
        )

        annual_leaves: int = round(balance.annual_leaves / 12 * month)
        leave_excuses: int = round(balance.leave_excuses / 12 * month)
        emergency_leaves: int = round(balance.emergency_leaves / 12 * month)
        calculated_values = {
            "annual_leaves": annual_leaves,
            "leave_excuses": leave_excuses,
            "emergency_leaves": emergency_leaves,
            "sick_leaves": balance.sick_leaves,
            "unpaid": balance.unpaid,
            "compensation": balance.compensation,
        }
        return calculated_values

    def create_new_balance(self, user: User) -> VacationBalance:
        """
        Use a dict of calculated values based on joining date
        to create a vacation balance object for a user.
        Some Values are static and does not depend on
        joining date like i.e sick_leaves.
        """
        values: Dict = self.create_new_balance_values(user=user)
        balance: VacationBalance = VacationBalance.objects.create(
            user=user,
            annual_leaves=values["annual_leaves"],
            compensation=values["compensation"],
            sick_leaves=values["sick_leaves"],
            emergency_leaves=values["emergency_leaves"],
            leave_excuses=values["leave_excuses"],
            unpaid=values["unpaid"],
            actual_balance=values,
        )

        return balance

    def get_difference_between_two_days(self, start_date: datetime, end_date: datetime):
        return int((end_date - start_date).days + 1)

    def remove_weekends(self, user: User, start_date: datetime, end_date: datetime):
        weekend = user.location.weekend.split(":")
        delta = end_date - start_date  # returns timedelta
        actual_days = []
        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            if not day.strftime("%A") in weekend:
                actual_days.append(day)
        return actual_days

    def remove_holidays(
        self,
        user: User,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        dates: List[datetime.date],
    ):
        removed_weekends = self.remove_weekends(user, start_date, end_date)
        years = [start_date.year, end_date.year]
        months = [start_date.month, end_date.month]
        holidays = get_user_holidays(years, months)
        _holydays = 0

        for date in removed_weekends:
            if date not in dates:
                dates.append(date)

        for day in holidays:
            if day.holiday_date in removed_weekends:
                _holydays += 1

        return len(dates) - _holydays

    def vacation_update_balance(self, vacation: Vacation):
        """
        This method will used when user wants to update his vacation request and the reaseon changed.
        the actual value of old reason must return.
        """
        old_days: int = self.remove_weekends(
            vacation.applying_user, vacation.from_date, vacation.end_date
        )
        old_days = self.remove_holidays(
            vacation.applying_user, vacation.from_date, vacation.end_date, old_days
        )

        reason: str = vacation.reason
        this_month: int = datetime.datetime.now().month
        balance: VacationBalance = VacationBalance.objects.get(
            user=vacation.applying_user
        )
        get_actual_reason_value = getattr(balance, reason)
        if vacation.taked_from_old_balance and this_month < 3:
            return self.update_user_balance(
                vacation.applying_user,
                reason,
                balance.old_balance.get(reason) + old_days,
                taked_from_old_balance=vacation.taked_from_old_balance,
            )

        return self.update_user_balance(
            vacation.applying_user, reason, get_actual_reason_value + old_days
        )

    def check_balance(
        self,
        user: User,
        vacation: Vacation,
        reason: str,
        start_date: datetime,
        end_date: datetime,
    ):
        self.check(user)

        old_balance = self.check_old_balance(user, reason)
        v = user.vacationbalance
        vacation_days = self.remove_weekends(user, start_date, end_date)
        if hasattr(v, reason):
            curr_balance = getattr(v, reason)
            # if reason == "public_holidays":
            #     return "You cannot apply for public holidays vacations, you take it automatically."
            if old_balance + curr_balance >= len(vacation_days):
                new_value: int = curr_balance - len(vacation_days)
                this_month: int = datetime.datetime.now().month
                if old_balance >= len(vacation_days) and this_month < 3:
                    self.set_taked_from_old_balance(vacation)
                    return self.update_user_balance(
                        user,
                        reason,
                        old_balance - len(vacation_days),
                        taked_from_old_balance=vacation.taked_from_old_balance,
                    )
                return self.update_user_balance(user, reason, new_value)
            return f"You only have {old_balance+curr_balance} days left of reason '{reason.capitalize().replace('_', ' ')}'"

    def set_taked_from_old_balance(self, vacation: Vacation):
        """Update vacation with taked from ild balance to return the value to old balance when user update his request."""
        vacation.taked_from_old_balance = True
        vacation.save()

    def update_user_balance(
        self,
        user: User,
        reason: REASON_CHOICES,
        new_value: int,
        taked_from_old_balance: bool = False,
    ) -> VacationBalance:
        """
        Set new value based on field name -> reason.
        user: Current user.
        reason: one of 'VacationBalance' fields.
        new_value: the new value will adding to filed[reason]
        """
        balance: VacationBalance = VacationBalance.objects.get(user=user)
        if taked_from_old_balance:
            if reason in balance.old_balance:
                balance.old_balance[reason] = new_value
                balance.save()
                return True
            return f"Old balance has no attrbute named {reason}"

        if hasattr(balance, reason):
            setattr(balance, reason, new_value)
            balance.save()
            return True
        return f"There is no filed or attrbute named {reason} inside VacationBalance model."

    def check_old_balance(self, user: User, reason: str):
        """
        This function gives you the balance value of a specific
        reason e.g "annual_leaves" in the given object's old balance field.
        if it's empty then it will return 0
        """
        if (
            user.vacationbalance.old_balance == {}
            or user.vacationbalance.old_balance[reason] == 0
        ):
            return 0
        else:
            return user.vacationbalance.old_balance[reason]

    def old_balance_format(self, user: User) -> VacationBalance:
        """
        This function takes a user as an argument and
        based on the json file it will make a similar one
        to be stored on the old_balance field for vacation balance model.
        This function should run by the end of every year to update
        the old_balance field.
        """
        user_balance = self.check(user)
        balance_format = {}
        balance_format["annual_leaves"] = user_balance.annual_leaves
        balance_format["sick_leaves"] = user_balance.sick_leaves
        balance_format["compensation"] = user_balance.compensation
        balance_format["unpaid"] = user_balance.unpaid
        balance_format["emergency_leaves"] = user_balance.emergency_leaves
        balance_format["leave_execuses"] = user_balance.leave_execuses
        balance_format["year"] = user_balance.date.year

        balance: VacationBalance = VacationBalance.objects.get(user=user)
        balance.old_balance = balance_format
        balance.save()
        return balance_format

    def resetting_old_balance(self, user: User):
        """ "
        This function should run annualy at april to reset
        the old_balance field to an empty directory
        """
        balance: VacationBalance = VacationBalance.objects.get(user=user)
        balance.old_balance = {}
        balance.save()
