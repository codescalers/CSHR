from typing import List
from cshr.models.vacations import PublicHoliday
from datetime import datetime


def filter_public_holidays_by_month_and_year(year: str, month: str):
    """
    Filter holidays based on the year and month to be displayed on the calander.
    """
    return PublicHoliday.objects.filter(
        holiday_date__year=year, holiday_date__month=month
    )


def get_user_holidays(years: List[int], months: List[int]):
    """
    Filter holidays based on user location and the year and month to be displayed on the calander.
    """
    today = datetime.now()
    holidays = PublicHoliday.objects.filter(
        holiday_date__year__in=years,
        holiday_date__month__in=months,
        expired=False,
    )

    for date in holidays:
        if date.holiday_date.day < today.day:
            date.expired = True
            date.save()

    return holidays
