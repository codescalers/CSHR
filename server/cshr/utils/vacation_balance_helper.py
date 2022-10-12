from typing import Any, Dict, List
from server.cshr.api.response import CustomResponse
from server.cshr.models.users import User
from server.cshr.models.vacations import REASON_CHOICES, VacationBalance

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
        founded: bool = self.file_content.get(key)
        if founded:
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
        leave_execuses: int = round(self.file_content["leave_execuses"] / 12 * month)
        emergency_leaves: int = round(
            self.file_content["emergency_leaves"] / 12 * month
        )
        calculated_values = {
            "annual_leaves": annual_leaves,
            "leave_execuses": leave_execuses,
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
                leave_execuses=values["leave_execuses"],
                unpaid=values["unpaid"],
            ),
        )
        return balance[0]  # Create returns an instance of tuple

    def get_difference_between_two_days(self, start_date: datetime, end_date: datetime):
        return int((end_date - start_date).days + 1)

    def check_balance(self, user, reason, start_date: datetime, end_date: datetime):
        self.check(user)
        old_balance = self.check_old_balance(user, reason)
        v = user.vacationbalance
        vacation_days = self.get_difference_between_two_days(start_date, end_date)
        if hasattr(v, reason):
            curr_balance = getattr(v, reason)
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


# from server.cshr.models.users import User
# from server.cshr.api.response import CustomResponse
# from typing import Any, Dict, List
# from server.cshr.models.vacations import VacationBalance, PublicHolidays
# import os
# import json
# import calendar
# import datetime
# from django.db.models import Q
# from datetime import timedelta, date


# class VacationBalanceHelper:
#     def __init__(self):
#         self.abspath = os.path.abspath(os.path.dirname(__file__))
#         self.file_path = os.path.join(f"{self.abspath}/vacation_balance.json")
#         self.file_content = self.read_file()

#     def read_file(self):
#         """
#         this function reads the json file in this directory.
#         it assumes its name will be vacation_balance.json
#         """
#         with open(self.file_path, "r") as f:
#             self.file_content = json.loads(f.read())
#             f.close()
#         return self.file_content

#     def myconverter(self, o):
#         if isinstance(o, datetime.datetime):
#             return o.__str__()

#     def bulk_write(self, content: Dict) -> Dict:
#         if not type(content) == dict:
#             return CustomResponse.bad_request("Balance argument must be a dict.")
#         with open(self.file_path, "w") as f:
#             f.write(json.dumps(content))
#             self.file_content = content
#             f.close()
#         return self.file_content

#     def write(self, key: str, new_value: Any) -> Dict:
#         """Write method that can write new values into balance Json file."""
#         founded: bool = self.file_content.get(key)
#         if founded:
#             self.file_content[key] = new_value
#         return self.bulk_write(self.file_content)

#     def calculate_public_holidays(self, public_holidays: List, created_at: datetime):
#         """
#         This function takes a list of dates as public holidays,
#         based on joinig date it will calculate how much days you deserve
#         """
#         for ph in public_holidays:
#             PublicHolidays.objects.create(date=datetime.datetime.fromisoformat(ph).date())
#         return PublicHolidays.objects.filter(date__gte=created_at).count()

#     def old_balance_format(self, user: User) -> VacationBalance:
#         """
#         This function takes a user as an argument and
#         based on the json file it will make a similar one
#         to be stored on the old_balance field for vacation balance model.
#         This function should run by the end of every year to update
#         the old_balance field.
#         """
#         user_balance = self.check(user)
#         balance_format = self.read_file()
#         balance_format["annual_leaves"] = user_balance.annual_leaves
#         balance_format["sick_leaves"] = user_balance.sick_leaves
#         balance_format["compensation"] = user_balance.compensation
#         balance_format["unpaid"] = user_balance.unpaid
#         balance_format["emergency_leaves"] = user_balance.emergency_leaves
#         balance_format["leave_execuses"] = user_balance.leave_execuses
#         balance_format["public_holidays"] = {}
#         balance_format["year"] = user_balance.date.year
#         user.vacationbalance.old_balance = balance_format
#         user.save()
#         return balance_format

#     # def check_year_and_run_task implement this function to create new task [andrew will do it],
#     #  this task will run every year to delete the old balance from user ld balance

#     def resetting_old_balance(self, user: User):
#         """ "
#         This function should run annualy at april to reset
#         the old_balance field to an empty directory
#         """
#         user.vacationbalance.old_balance = {}

#     def check_old_balance(self, user: User, type: str):
#         """
#         This function gives you the balance value of a specific
#         type e.g "annual_leaves" in the given object's old balance field.
#         if it's empty then it will return 0
#         """
#         if (
#             user.vacationbalance.old_balance == {}
#             or user.vacationbalance.old_balance[type] == 0
#         ):
#             return 0
#         else:
#             return user.vacationbalance.old_balance[type]

#     def update_json_format(self, obj: VacationBalance, key: str, value: str):
#         """
#         This function updates a given value of the old_balance dict
#         and save the updated dict on the database.
#         """
#         obj.old_balance[key] = value
#         setattr(obj, "old_balance", obj.old_balance)
#         obj.save()
#         return obj.old_balance[key]

#     def calculate_vacation_values(self, created_at: datetime) -> Dict:
#         """
#         This function helps when calculating the user vacation balance
#         values based on the joining date and the given Json file.
#         """
#         month_helper_constant = 12 - created_at.month + 1
#         calculated_values = {
#             "annual_leaves": (self.file_content["annual_leaves"] / 12) * month_helper_constant,
#             "emergency_leaves": (self.file_content["emergency_leaves"] / 12) * month_helper_constant,
#             "leave_execuses": (self.file_content["leave_execuses"] / 12) * month_helper_constant,
#             "sick_leaves": self.file_content["sick_leaves"],
#             "compensation": self.file_content["compensation"],
#             "unpaid": self.file_content["unpaid"],
#             "public_holidays": self.calculate_public_holidays(self.file_content["public_holidays"], created_at),
#         }
#         return calculated_values

#     def update_all_users_balance(self):
#         calculated_values = self.calculate_vacation_values(date(date.today().year, 1, 1))
#         users = User.objects.filter(~Q(created_at__year=self.read_file()["year"]))

#         for u in users:
#             v = u.vacationbalance
#             v.annual_leaves = round(calculated_values["annual_leaves"], 1)
#             v.compensation = round(calculated_values["compensation"], 1)
#             v.sick_leaves = round(calculated_values["sick_leaves"], 1)
#             v.emergency_leaves = round(calculated_values["emergency_leaves"], 1)
#             v.public_holidays = round(calculated_values["public_holidays"], 1)
#             v.leave_execuses = round(calculated_values["leave_execuses"], 1)
#             v.unpaid = round(calculated_values["unpaid"], 1)
#             v.save()

#     def get_difference_between_two_days(self, start_date: datetime, end_date: datetime):
#         return int((end_date - start_date).days + 1)

#     def check_balance(self, user, reason, start_date: datetime, end_date: datetime):
#         old_balance = self.check_old_balance(user, reason)
#         v = user.vacationbalance
#         vacation_days = self.get_difference_between_two_days(start_date, end_date)
#         print(dir(v))
#         if hasattr(v, reason):
#             curr_balance = getattr(v, reason)
#             print(user.vacationbalance.emergency_leaves)
#             print(old_balance ,curr_balance, vacation_days)
#             if old_balance + curr_balance >= vacation_days:
#                 return True
#             return f"You only have {old_balance+curr_balance} days left of reason {reason}"

#     def check(self, user) -> VacationBalance:
#         """
#         This function simply checks if a user has a vacationbalance object
#         if not it wiil create one and return it otherwise it will return it.
#         """
#         print("+" * 500)
#         try:
#             return VacationBalance.objects.get(user=user)
#         except VacationBalance.DoesNotExist:
#             return self.create(user)

#     def create(self, user: User) -> VacationBalance:
#         """
#         Use a dict of calculated values based on joining date
#         to create a vacation balance object for a user.
#         Some Values are static and does not depend on
#         joining date like i.e sick_leaves.
#         """
#         calaculated_values = self.calculate_vacation_values(user.created_at)
#         VacationBalance.objects.create(
#             user=user,
#             annual_leaves=round(calaculated_values["annual_leaves"]),
#             compensation=round(calaculated_values["compensation"]),
#             sick_leaves=round(calaculated_values["sick_leaves"]),
#             emergency_leaves=round(calaculated_values["emergency_leaves"]),
#             public_holidays=round(calaculated_values["public_holidays"]),
#             leave_execuses=round(calaculated_values["leave_execuses"]),
#             unpaid=round(calaculated_values["unpaid"]),
#         ),

#         return VacationBalance.objects.get(user=user)

#     def update_balance(self, type: str, obj: VacationBalance, new_value: int) -> VacationBalance:
#         """
#         Set new value based on field name -> type.
        #: one of 'VacationBalance' fields.
#         obj: `VacationBalance` instance.
#         new_value: the new value will adding to filed[type]
#         """
#         if hasattr(obj, type):
#             setattr(obj, type, new_value)
#             obj.save()
#             return getattr(obj, type)
#         return

#     def calculate_balance(self, v: VacationBalance, value: str, type: str):
#         if hasattr(v, type):
#             balance_value = getattr(v, type)
#         if value <= balance_value:
#             new_value = balance_value - value
#             return self.update_balance(type, v, new_value)
#         return "No Enough balance"
#         # what if the required vacation balance is more than the current balance

#     def calculate_public_and_official_holidays(self, user: User, start_date: datetime, vacation_days: int):

#         public_holidays_count = 0
#         official_holidays_count = 0
#         official_holidays = user.location.official_holidays
#         for n in range(vacation_days):
#             curr_date = start_date + timedelta(n)

#             public_holidays_count += PublicHolidays.objects.filter(
#                 date__day=curr_date.day,
#                 date__month=curr_date.month,
#                 date__year=curr_date.year,
#             ).count()
#             if (
#                 calendar.day_name[curr_date.weekday()] in official_holidays
#                 and PublicHolidays.objects.filter(
#                     date__day=curr_date.day,
#                     date__month=curr_date.month,
#                     date__year=curr_date.year,
#                 ).exists()
#             ):
#                 public_holidays_count -= 1
#             if calendar.day_name[curr_date.weekday()] in official_holidays:
#                 official_holidays_count += 1

#         return public_holidays_count + official_holidays_count

#     def apply_for_vacation(
#         self,
#         user: User,
#         start_date: datetime,
#         end_date: datetime,
#         type: str,
#     ):
#         vacation_days = self.get_difference_between_two_days(start_date, end_date)
#         value = vacation_days
#         if value <= 0:
#             return "Invalid Input"
#         type_old_balance = self.check_old_balance(user, type)
#         public_official_holidays_count = self.calculate_public_and_official_holidays(user, start_date, vacation_days)

#         value = value - public_official_holidays_count

#         if type_old_balance == 0:
#             return self.calculate_balance(user.vacationbalance, value, type)
#         elif value <= type_old_balance:
#             type_old_balance -= value
#             return self.update_json_format(user.vacationbalance, type, type_old_balance)

#         elif value > type_old_balance:
#             value = value - type_old_balance
#             self.update_json_format(user.vacationbalance, type, 0)
#             if value > 0:
#                 return self.calculate_balance(user.vacationbalance, value, type)
