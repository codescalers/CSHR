from typing import Any, Dict, List
from server.cshr.api.response import CustomResponse
from server.cshr.models.users import User
from server.cshr.models.vacations import REASON_CHOICES, Vacation, VacationBalance

import datetime
import os
import json


class StanderdVacationBalance:
    def __init__(self):
        self.abspath = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(f"{self.abspath}/vacation_balance.json")
        self.file_content = self.read_file()
        self.emergency_year: int = 6
        self.emergency_month: int = 2
        self.extra_emergency: int = 1.5  # From annual balance.

    def read_file(self):
        """
        this function reads the json file in this directory.
        it assumes its name will be vacation_balance.json
        """
        with open(self.file_path, "r") as f:
            self.file_content = json.loads(f.read())
            f.close()
        return self.file_content

    def write(self, key: str, new_value: Any) -> Dict:
        """Write method that can write new values into balance Json file."""
        founded: Any = self.file_content.get(key)
        if founded is not None:
            self.file_content[key] = new_value
        return self.bulk_write(self.file_content)

    def bulk_write(self, content: Dict) -> Dict:
        if not type(content) == dict:
            return CustomResponse.bad_request(
                message="Invalid type {}".format(type(content))
            )

        with open(self.file_path, "w") as f:
            f.write(json.dumps(content))
            self.file_content = content
            f.close()
        return self.file_content

    def check(self, user) -> VacationBalance:
        try:
            return VacationBalance.objects.get(user=user)
        except VacationBalance.DoesNotExist:
            return self.create_new_balance(user)

    def set_public_holidays(self, user):
        """
        Calculate and set the public holidays for the user,
        .e.g. user who came at 7 of october not alled to tace this day.
        """
        user_joining_date: int = user.created_at
        public_holidays: List[str] = self.file_content.get("public_holidays")
        response_public_holidays: List[str] = []
        today: datetime = datetime.datetime.today()
        for day in public_holidays:
            splited_day: List[str] = day.split("-")
            formated_day: datetime = datetime.datetime(
                year=int(splited_day[0]),
                month=int(splited_day[1]),
                day=int(splited_day[2]),
            )
            if formated_day.year == today.year:
                if (
                    formated_day.day >= user_joining_date.day
                    and formated_day.month >= user_joining_date.month
                ):
                    response_public_holidays.append(formated_day.date())
        return response_public_holidays

    def create_new_balance_values(self, user: User) -> Dict:
        # this help to divide to get the total days based on joining date
        month: int = 12 - user.created_at.month

        annual_leaves: int = round(self.file_content["annual_leaves"] / 12 * month)
        leave_excuses: int = round(self.file_content["leave_excuses"] / 12 * month)
        emergency_leaves: int = round(
            self.file_content["emergency_leaves"] / 12 * month
        )
        calculated_values = {
            "annual_leaves": annual_leaves,
            "leave_excuses": leave_excuses,
            "emergency_leaves": emergency_leaves,
            "sick_leaves": self.file_content["sick_leaves"],
            "unpaid": self.file_content["unpaid"],
            "compensation": self.file_content["compensation"],
            "public_holidays": len(self.set_public_holidays(user)),
            "year": self.file_content["year"],
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
        balance: VacationBalance = (
            VacationBalance.objects.create(
                user=user,
                annual_leaves=values["annual_leaves"],
                compensation=values["compensation"],
                sick_leaves=values["sick_leaves"],
                emergency_leaves=values["emergency_leaves"],
                public_holidays=values["public_holidays"],
                leave_excuses=values["leave_excuses"],
                unpaid=values["unpaid"],
            ),
        )
        return balance[0]  # Create returns an instance of tuple

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
        return len(actual_days)
    
    def vacation_update_balance(self, vacation: Vacation):
        """
            This method will used when user wants to update his vacation request and the reaseon changed.
            the actual value of old reason must return.
        """ 
        old_days: int = self.remove_weekends(
            vacation.applying_user, vacation.from_date, vacation.end_date
        )
        reason: str = vacation.reason
        balance: VacationBalance = VacationBalance.objects.get(user=vacation.applying_user)
        get_actual_reason_value = getattr(balance, reason)
        return self.update_user_balance(vacation.applying_user, reason, get_actual_reason_value + old_days)

    def check_balance(self, user, reason, start_date: datetime, end_date: datetime):
        self.check(user)

        old_balance = self.check_old_balance(user, reason)
        v = user.vacationbalance
        vacation_days = self.remove_weekends(user, start_date, end_date)
        if hasattr(v, reason):
            curr_balance = getattr(v, reason)
            if reason == "public_holidays":
                return "You cannot apply for public holidays vacations, you take it automatically."
            if old_balance + curr_balance >= vacation_days:
                new_value: int = curr_balance - vacation_days
                return self.update_user_balance(user, reason, new_value)
            return (
                f"You only have {old_balance+curr_balance} days left of reason {reason}"
            )

    def update_user_balance(
        self, user: User, reason: REASON_CHOICES, new_value: int
    ) -> VacationBalance:
        """
        Set new value based on field name -> reason.
        user: Current user.
        reason: one of 'VacationBalance' fields.
        new_value: the new value will adding to filed[reason]
        """
        balance: VacationBalance = VacationBalance.objects.get(user=user)
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
        balance_format = self.read_file()
        balance_format["annual_leaves"] = user_balance.annual_leaves
        balance_format["sick_leaves"] = user_balance.sick_leaves
        balance_format["compensation"] = user_balance.compensation
        balance_format["unpaid"] = user_balance.unpaid
        balance_format["emergency_leaves"] = user_balance.emergency_leaves
        balance_format["leave_execuses"] = user_balance.leave_execuses
        balance_format["public_holidays"] = {}
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