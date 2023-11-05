
from typing import List
from server.cshr.models.office import Office
from server.cshr.models.users import User
from server.cshr.models.vacations import PublicHoliday


def filter_public_holidays_by_month_and_year(year: str, month: str):
  """
    Filter holidays based on the year and month to be displayed on the calander.
  """
  return PublicHoliday.objects.filter(holiday_date__year=year, holiday_date__month=month)

def get_user_holidays(user: User, years: List[int], months: List[int]):
  """
    Filter holidays based on user location and the year and month to be displayed on the calander.
  """
  location: Office = user.location
  return PublicHoliday.objects.filter(
    location=location,
    holiday_date__year__in=years,
    holiday_date__month__in=months
  )