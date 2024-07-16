from typing import List
from cshr.models.vacations import PublicHoliday
from datetime import datetime

from cshr.models.office import Office


def filter_public_holidays_by_month_and_year(year: str, month: str):
    """
    Filter holidays based on the year and month to be displayed on the calander.
    """
    return PublicHoliday.objects.filter(
        holiday_date__year=year, holiday_date__month=month
    )


def filter_office_public_holidays_based_on_dates(location: Office, dates: List[datetime]) -> List[PublicHoliday]:
    """
    Filter holidays based on the provided dates' years and months, and mark past holidays as expired.
    """
    if not dates:
        return []

    today = datetime.now()
    years = set(date.year for date in dates)
    months = set(date.month for date in dates)

    holidays = PublicHoliday.objects.filter(
        holiday_date__year__in=years,
        holiday_date__month__in=months,
        location__id=location.pk,
    )

    for holiday in holidays:
        if holiday.holiday_date < today.date():
            holiday.expired = True
            holiday.save()

    return holidays