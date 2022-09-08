from server.cshr.models.users import User
from server.cshr.api.response import CustomResponse
from typing import Dict
from server.cshr.models.vacation_balance import VacationBalance
import os, json


class VacationBalanceHelper:
    def __init__(self):
        self.abspath = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(f'{self.abspath}/vacation_balance.json')

    def read(self):
        with open(self.file_path, 'r') as f:
            self.file = f
            self.balance = json.loads(f.read())
            f.close()
        return self.balance

    def write(self, balance: Dict) -> Dict:
        """Write method that can write new values into balance file."""
        if not type(balance) == dict:
            return CustomResponse.bad_request("Balance argument must be a dict.")
        self.balance = balance
        with open(self.file_path, 'r+') as f:
            f.write(json.dumps(balance))
            self.balance = self.read()
            f.close()
        return balance

    def check_or_create(self, user: User) -> VacationBalance:
        """Check if user has vacation balance object in database"""
        return VacationBalance.objects.get_or_create(user=user)

    def old_balance_format(self, user: User) -> VacationBalance:
        user_balance = self.check_or_create(user)[0]
        balance_format = self.read()
        balance_format["annual_leaves"] = user_balance.annual_leaves
        balance_format["sick_leaves"] = user_balance.sick_leaves
        balance_format["compensation"] = user_balance.compensation
        balance_format["unpaid"] = user_balance.unpaid
        balance_format["emergencies"] = user_balance.emergencies
        balance_format["leave_execuses"] = user_balance.leave_execuses
        balance_format["public_holidays"] = user_balance.public_holidays
        balance_format["year"] = user_balance.date.year
        return balance_format
    
    # def check_year_and_run_task implement this function to create new task [andrew will do it], this task will run every year to delete the old balance from user ld balance
    
    def update_json_format(self, obj: VacationBalance, key: str, value: str):
        obj[key] = value


    # def calculate_vacation_values(self, user: User) -> Dict:
    #     # this help to divide to get the total days based on joining date
    #     month_helper_constant = 12 - user.created_at.month - 1
    #     calculated_values = {
    #         "annual_leaves": self.__annual_leaves__ / month_helper_constant,
    #         "emergencies": self.__emergencies__ / month_helper_constant,
    #         "leave_execuses": self.__emergencies__ / month_helper_constant,
    #     }
    #     return calculated_values

    # def check(self, user) -> VacationBalance:
    #     try:
    #         return VacationBalance.objects.get(user=user)
    #     except VacationBalance.DoesNotExist:
    #         return self.create(user)

    # def create(self, user: User) -> VacationBalance:
    #     calaculated_values = self.calculate_vacation_values(user=user)
    #     balance: VacationBalance = (
    #         VacationBalance.objects.create(
    #             user=user,
    #             annual_leaves=calaculated_values["annual_leaves"],
    #             compensation=self.__compensation__,
    #             sick_leaves=self.__sick_leaves__,
    #             emergencies=self.__emergencies__,
    #             public_holidays=self.__public_holidays__,
    #             leave_execuses=calaculated_values["leave_execuses"],
    #             unpaid=self.__unpaid__,
    #         ),
    #     )
    #     return balance

    # def update(self, type: str, obj: VacationBalance, new_value: int ) -> VacationBalance:
    #     """
    #         Set new value based on field name -> type.
    #         type: one of 'VacationBalance' fields.
    #         obj: `VacationBalance` instance.
    #         new_value: the new value will adding to filed[type]
    #     """
    #     if hasattr(obj, type):
    #         setattr(obj, type, new_value)
    #         obj.save()
    #         return obj
    #     return

    #     2/15