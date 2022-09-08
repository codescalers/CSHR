from server.cshr.models.users import User
from typing import Dict
from server.cshr.models.vacation_balance import VacationBalance


class VacationBalanceHelper:
    def __init__(self):
        self.__annual_leaves__ = 15
        self.__sick_leaves__ = 100
        self.__compensation__ = 0
        self.__unpaid__ = 0
        self.__emergencies__ = 6
        self.__leave_execuses__ = 3
        self.__public_holidays__ = 0  # input from admin.

    def calculate_vacation_values(self, user: User) -> Dict:
        # this help to divide to get the total days based on joining date
        month_helper_constant = 12 - user.created_at.month - 1
        calculated_values = {
            "annual_leaves": self.__annual_leaves__ / month_helper_constant,
            "emergencies": self.__emergencies__ / month_helper_constant,
            "leave_execuses": self.__emergencies__ / month_helper_constant,
        }
        return calculated_values

    def check(self, user) -> VacationBalance:
        try:
            return VacationBalance.objects.get(user=user)
        except VacationBalance.DoesNotExist:
            return self.create(user)

    def create(self, user: User) -> VacationBalance:
        calaculated_values = self.calculate_vacation_values(user=user)
        balance: VacationBalance = (
            VacationBalance.objects.create(
                user=user,
                annual_leaves=calaculated_values["annual_leaves"],
                compensation=self.__compensation__,
                sick_leaves=self.__sick_leaves__,
                emergencies=self.__emergencies__,
                public_holidays=self.__public_holidays__,
                leave_execuses=calaculated_values["leave_execuses"],
                unpaid=self.__unpaid__,
            ),
        )
        return balance
    def update(self, type: str, obj: VacationBalance, new_value: int ) -> VacationBalance:
        types = {
            "annual_leaves": obj.annual_leaves,
            "sick_leaves": obj.sick_leaves,
            "compensation": obj.compensation,
            "unpaid": obj.unpaid,
            "emergencies": obj.emergencies,
            "leave_execuses": obj.leave_execuses,
            "public_holidays": obj.public_holidays,
        }
        types[type] = new_value
        field = VacationBalance._meta.get_field(type)
        print(obj[field])
        obj.field = new_value
        obj.save()
        return obj