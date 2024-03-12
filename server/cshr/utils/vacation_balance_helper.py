from typing import List
from cshr.models.requests import STATUS_CHOICES
from cshr.models.users import User
from cshr.models.vacations import (
    REASON_CHOICES,
    OfficeVacationBalance,
    Vacation,
    VacationBalance,
)

import datetime

from cshr.services.public_holidays import get_user_holidays


class StanderdVacationBalance:
    def check(self, user) -> VacationBalance:
        self.user = user
        balance = VacationBalance.objects.filter(user=self.user)
        if(len(balance) == 0):
            balance = self.create_new_balance()
        else:
            balance = balance[0]
            if balance.office_vacation_balance is None:
                office_balance = OfficeVacationBalance.objects.get_or_create(
                    year=datetime.datetime.now().year, location=self.user.location
                )[0]
                balance.office_vacation_balance = office_balance
                balance.save()

        return None if balance is None else balance

    def create_new_balance(self):
        if self.user is None or self.user.location.id is None:
            return None

        month: int = 12
        if self.user.joining_at.month > 1:
            month: int = 12 - self.user.joining_at.month

        office_balance = OfficeVacationBalance.objects.get_or_create(
            year=datetime.datetime.now().year, location=self.user.location
        )[0]

        annual_leaves: int = round(office_balance.annual_leaves / 12 * month)
        leave_excuses: int = round(office_balance.leave_excuses / 12 * month)
        emergency_leaves: int = round(office_balance.emergency_leaves / 12 * month)

        balance: VacationBalance = VacationBalance.objects.get_or_create(
            user=self.user,
            annual_leaves=annual_leaves,
            compensation=office_balance.compensation,
            sick_leaves=office_balance.sick_leaves,
            emergency_leaves=emergency_leaves,
            leave_excuses=leave_excuses,
            unpaid=office_balance.unpaid,
            office_vacation_balance = office_balance
        )[0]

        return balance

    def update_user_balance(
        self,
        applying_user: User,
        reason: REASON_CHOICES,
        new_value: int,
    ) -> VacationBalance:
        """
        Set new value based on field name -> reason.
        user: Applying user.
        reason: one of 'VacationBalance' fields.
        new_value: the new value will adding to filed[reason]
        """
        balance: VacationBalance = VacationBalance.objects.get(user=applying_user)

        if hasattr(balance, reason):
            setattr(balance, reason, new_value)
            balance.save()
            return True
        return f"There is no filed or attrbute named {reason} inside VacationBalance model."

    def get_actual_days(
        self, user: User, start_date: datetime, end_date: datetime
    ) -> int:
        days = self.__remove_weekends(user, start_date, end_date)
        days = self.remove_holidays(user, start_date, end_date, days)
        return days

    def check_and_update_balance(
        self,
        applying_user: User,
        vacation: Vacation,
        reason: str,
        start_date: datetime,
        end_date: datetime,
    ):
        if reason == "public_holidays":
            return "You cannot apply for public holidays vacations, you take it automatically."

        self.check(applying_user)
        v = applying_user.vacationbalance
        vacation_days = self.get_actual_days(applying_user, start_date, end_date)

        if hasattr(v, reason):
            curr_balance = getattr(v, reason)
            if curr_balance >= vacation_days:
                if vacation.status == STATUS_CHOICES.PENDING:
                    new_value: int = curr_balance - vacation_days
                    return self.update_user_balance(applying_user, reason, new_value)
                return f"The vacation status is not pending, it's {vacation.status}."
            return f"You only have {curr_balance} days left of reason '{reason.capitalize().replace('_', ' ')}'"
        return "Unknown reason."

    def get_difference_between_two_days(self, start_date: datetime, end_date: datetime) -> int:
        return int((end_date - start_date).days + 1)
    
    def __remove_weekends(self, user: User, start_date: datetime, end_date: datetime) -> List[int]:
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
    ) -> int:
        removed_weekends = self.__remove_weekends(user, start_date, end_date)
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