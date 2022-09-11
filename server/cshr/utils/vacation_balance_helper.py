from server.cshr.models.users import User
from server.cshr.api.response import CustomResponse
from typing import Dict, List
from server.cshr.models.vacations import VacationBalance, PublicHolidays
import os
import json
import datetime


class VacationBalanceHelper:
    def __init__(self):
        self.abspath = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(f"{self.abspath}/vacation_balance.json")

    def read(self):
        """
        this function reads the json file in this directory.
        it assumes its name will be vacation_balance.json
        """
        with open(self.file_path, "r") as f:
            self.file = f
            self.balance = json.loads(f.read())
            f.close()
        return self.balance

    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def write(self, balance: Dict) -> Dict:
        """Write method that can write new values into balance Json file."""
        if not type(balance) == dict:
            return CustomResponse.bad_request("Balance argument must be a dict.")
        self.balance = balance
        with open(self.file_path, "r+") as f:
            f.write(json.dumps(balance, default=self.myconverter))
            self.balance = self.read()
            f.close()
        return balance

    def calculate_public_holidays(self, public_holidays: List, user: User):
        """
        This function takes a list of dates as public holidays,
        based on joinig date it will calculate how much days you deserve
        """
        for ph in public_holidays:
            PublicHolidays.objects.create(
                date=datetime.datetime.fromisoformat(ph).date()
            )
        return PublicHolidays.objects.filter(date__gte=user.created_at).count()

    def old_balance_format(self, user: User) -> VacationBalance:
        """
        This function takes a user as an argument and
        based on the json file it will make a similar one
        to be stored on the old_balance field for vacation balance model.
        This function should run by the end of every year to update
        the old_balance field.
        """
        user_balance = self.check(user)
        balance_format = self.read()
        balance_format["annual_leaves"] = user_balance.annual_leaves
        balance_format["sick_leaves"] = user_balance.sick_leaves
        balance_format["compensation"] = user_balance.compensation
        balance_format["unpaid"] = user_balance.unpaid
        balance_format["emergencies"] = user_balance.emergencies
        balance_format["leave_execuses"] = user_balance.leave_execuses
        balance_format["public_holidays"] = user_balance.public_holidays
        balance_format["year"] = user_balance.date.year
        user.vacationbalance.old_balance = balance_format
        user.save()
        return balance_format

    # def check_year_and_run_task implement this function to create new task [andrew will do it],
    #  this task will run every year to delete the old balance from user ld balance

    def resetting_old_balance(self, user: User):
        """ "
        This function should run annualy at april to reset
        the old_balance field to an empty directory
        """
        user.vacationbalance.old_balance = {}

    def check_old_balance(self, user: User, type: str):
        """
        This function gives you the balance value of a specific
        type e.g "annual_leaves" in the given object's old balance field.
        if it's empty then it will return 0
        """
        if user.vacationbalance.old_balance == {}:
            return 0
        else:
            return user.vacationbalance.old_balance[type]

    def update_json_format(self, obj: VacationBalance, key: str, value: str):
        """
        This function updates a given value of the old_balance dict
        and save the updated dict on the database.
        """
        obj.old_balance[key] = value
        setattr(obj, "old_balance", obj.old_balance)
        obj.save()

    def calculate_vacation_values(self, user: User) -> Dict:
        """
        This function helps when calculating the user vacation balance
        values based on the joining date and the given Json file.
        """
        month_helper_constant = 12 - user.created_at.month - 1
        calculated_values = {
            "annual_leaves": self.read()["annual_leaves"] / month_helper_constant,
            "emergencies": self.read()["emergencies"] / month_helper_constant,
            "leave_execuses": self.read()["leave_execuses"] / month_helper_constant,
            "sick_leaves": self.read()["sick_leaves"],
            "compensation": self.read()["compensation"],
            "unpaid": self.read()["unpaid"],
            "public_holidays": self.calculate_public_holidays(
                self.read()["public_holidays"], user
            ),
        }
        return calculated_values

    def check(self, user) -> VacationBalance:
        """
        This function simply checks if a user has a vacationbalance object
        if not it wiil create one and return it otherwise it will return it.
        """
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
            public_holidays=calaculated_values["public_holidays"],
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
