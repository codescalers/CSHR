from typing import List, Set
from cshr.models.requests import STATUS_CHOICES
from cshr.models.users import User
from cshr.models.vacations import (
    REASON_CHOICES,
    OfficeVacationBalance,
    Vacation,
    VacationBalance,
)

import datetime

from cshr.services.public_holidays import filter_office_public_holidays_based_on_dates


class StanderdVacationBalance:
    def check(self, user) -> VacationBalance:
        self.user = user
        balance = VacationBalance.objects.filter(user=self.user)
        if len(balance) == 0:
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

        annual_leaves: int = office_balance.annual_leaves / 12 * month
        leave_excuses: int = office_balance.leave_excuses / 12 * month
        emergency_leaves: int = office_balance.emergency_leaves / 12 * month

        balance: VacationBalance = VacationBalance.objects.get_or_create(
            user=self.user,
            annual_leaves=annual_leaves,
            compensation=office_balance.compensation,
            sick_leaves=office_balance.sick_leaves,
            emergency_leaves=emergency_leaves,
            leave_excuses=leave_excuses,
            unpaid=office_balance.unpaid,
            office_vacation_balance=office_balance,
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

    def calculate_times(self, start_hour: str, end_hour: str, CORE_HOURS=8) -> float:
        """Calculate the hours with the CORE_HOURS"""
        return (end_hour - start_hour) / CORE_HOURS

    def is_valid_times(
        self,
        times: float,
        start_hour: str,
        end_hour: str,
    ) -> bool:
        """
        Calculate the times and get the actual values, e.g. the start date is 11:0 AM, and the end date is 01:00 PM then the actual time should be 2 hours.
        """
        _times = self.calculate_times(start_hour=start_hour, end_hour=end_hour)
        return _times == times

    def get_actual_days(
        self, user: User, start_date: datetime, end_date: datetime
    ) -> int:
        dates: List[datetime.date] = self.remove_weekends(user, start_date, end_date)
        dates = self.remove_holidays(user, dates)
        return len(dates) if len(dates) > 0 else 0

    def check_and_update_balance(
        self,
        applying_user: User,
        vacation: Vacation,
        reason: str,
        start_date: datetime,
        end_date: datetime,
        delete: bool = False,
    ):
        if reason == "public_holidays":
            return "You cannot apply for public holidays vacations, you take it automatically."

        self.check(applying_user)
        v = applying_user.vacationbalance
        vacation_days = self.get_actual_days(applying_user, start_date, end_date)

        if hasattr(v, reason):
            curr_balance = getattr(v, reason)
            if vacation.status == STATUS_CHOICES.APPROVED:
                if delete:
                    new_value: int = curr_balance + vacation_days
                    return self.update_user_balance(applying_user, reason, new_value)
            if curr_balance >= vacation_days:
                if vacation.status == STATUS_CHOICES.PENDING:
                    new_value: int = curr_balance - vacation_days
                    return self.update_user_balance(applying_user, reason, new_value)
                return f"The vacation status is not pending, it's {vacation.status}."
            return f"You only have {curr_balance} days left of reason '{reason.capitalize().replace('_', ' ')}'"
        return "Unknown reason."

    def get_difference_between_two_days(self, start_date: datetime.datetime, end_date: datetime.datetime) -> int:
        return int((end_date - start_date).days + 1)
    
    def remove_weekends(self, user: User, start_date: datetime.datetime, end_date: datetime.datetime) -> List[datetime.datetime]:
        """
        Remove weekends from a range of dates based on the user's `office location`.

        This function filters out weekend days from the date range defined by the
        `start_date` and `end_date`. The weekends are determined by the `office location`
        specified in the user's profile.

        Args:
            user (`User`): The user whose `office location` is considered for determining weekends.
            start_date (`datetime`): The start date of the range.
            end_date (`datetime`): The end date of the range.

        Returns:
            List[`datetime`]: A list of dates excluding weekends.

        Raises:
            `ValueError`: If the start_date is after the end_date.
        """
        if start_date > end_date:
            raise ValueError("The start date cannot be after the end date.")

        weekend_days = user.location.weekend.lower().split(":") # e.g. Friday:Saturday
        delta = end_date - start_date  # returns timedelta
        actual_days = []

        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            if day.strftime("%A").lower() not in weekend_days:
                actual_days.append(day)
        return actual_days

    def remove_holidays(
        self,
        user: User,
        dates: List[datetime.date],
    ) -> List[datetime.date]:
        """
            Remove holidays from a list of dates based on the user's `office location`.

            This function filters out dates that fall on public holidays specific to the user's
            `office location`. The holidays are determined by the `office location` and the given
            dates.

            Args:
                user (User): The user whose `office location` is considered for determining holidays.
                dates (List[datetime.date]): A list of dates to be filtered.

            Returns:
                List[datetime.date]: A list of dates excluding those that are public holidays.

            Raises:
                ValueError: If the 'dates' list is empty.
        """
        if not dates:
            raise ValueError("The dates list cannot be empty.")

        holidays = filter_office_public_holidays_based_on_dates(user.location, dates)
        holiday_dates: Set[datetime.date] = {holiday.holiday_date for holiday in holidays}
        filtered_dates = [date for date in dates if date not in holiday_dates]

        return filtered_dates
