from server.cshr.models.users import User
from server.cshr.api.response import CustomResponse
from typing import Dict
from server.cshr.models.vacations import VacationBalance
import os
import json


class VacationBalanceHelper:
    def __init__(self):
        self.abspath = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(f"{self.abspath}/vacation_balance.json")

    def read(self):
        with open(self.file_path, "r") as f:
            self.file = f
            self.balance = json.loads(f.read())
            f.close()
        return self.balance

    def write(self, balance: Dict) -> Dict:
        """Write method that can write new values into balance file."""
        if not type(balance) == dict:
            return CustomResponse.bad_request("Balance argument must be a dict.")
        self.balance = balance
        with open(self.file_path, "r+") as f:
            f.write(json.dumps(balance))
            self.balance = self.read()
            f.close()
        return balance

    # def check_or_create(self, user: User) -> VacationBalance:
    #     """Check if user has vacation balance object in database"""
    #     return VacationBalance.objects.get_or_create(user=user)

    def old_balance_format(self, user: User) -> VacationBalance:
        user_balance = self.check(user)  # ?[0]
        balance_format = self.read()
        balance_format["annual_leaves"] = user_balance.annual_leaves
        balance_format["sick_leaves"] = user_balance.sick_leaves
        balance_format["compensation"] = user_balance.compensation
        balance_format["unpaid"] = user_balance.unpaid
        balance_format["emergencies"] = user_balance.emergencies
        balance_format["leave_execuses"] = user_balance.leave_execuses
        # balance_format["public_holidays"] = user_balance.public_holidays
        balance_format["year"] = user_balance.date.year
        user.vacationbalance.old_balance = balance_format
        user.save()
        return balance_format

    # def check_year_and_run_task implement this function to create new task [andrew will do it],
    #  this task will run every year to delete the old balance from user ld balance

    # should run annualy on april
    def resetting_old_balance(self, user: User):
        user.vacationbalance.old_balance = {}

    def check_old_balance_first(self, user: User, type: str):
        if user.vacationbalance.old_balance == {}:
            return 0
        else:
            return user.vacationbalance.old_balance[type]

    def update_json_format(self, obj: VacationBalance, key: str, value: str):
        obj.old_balance[key] = value

    def calculate_vacation_values(self, user: User) -> Dict:
        # this help to divide to get the total days based on joining date
        month_helper_constant = 12 - user.created_at.month - 1
        calculated_values = {
            "annual_leaves": self.read()["annual_leaves"] / month_helper_constant,
            "emergencies": self.read()["emergencies"] / month_helper_constant,
            "leave_execuses": self.read()["leave_execuses"] / month_helper_constant,
            "sick_leaves": self.read()["sick_leaves"],
            "compensation": self.read()["compensation"],
            "unpaid": self.read()["unpaid"],
            # "public_holidays": self.read()["public_holidays"],
        }
        return calculated_values

    def check(self, user) -> VacationBalance:
        try:
            return VacationBalance.objects.get(user=user)
        except VacationBalance.DoesNotExist:
            return self.create(user)

    def create(self, user: User) -> VacationBalance:
        """
        Use a dict of calculated values based on joining date
        to create a vacation balance object for a user.
        Some Values are static and does not depend on
        joining date like i.e sick_leaves.
        """
        calaculated_values = self.calculate_vacation_values(user=user)
        VacationBalance.objects.create(
            user=user,
            annual_leaves=calaculated_values["annual_leaves"],
            compensation=calaculated_values["compensation"],
            sick_leaves=calaculated_values["sick_leaves"],
            emergencies=calaculated_values["emergencies"],
            # public_holidays=calaculated_values["public_holidays"],
            leave_execuses=calaculated_values["leave_execuses"],
            unpaid=calaculated_values["unpaid"],
        ),

        return VacationBalance.objects.get(user=user)

    def update_balance(
        self, type: str, obj: VacationBalance, new_value: int
    ) -> VacationBalance:
        """
        Set new value based on field name -> type.
        type: one of 'VacationBalance' fields.
        obj: `VacationBalance` instance.
        new_value: the new value will adding to filed[type]
        """
        if hasattr(obj, type):
            setattr(obj, type, new_value)
            obj.save()
            return obj
        return
