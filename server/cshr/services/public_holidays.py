
from server.cshr.models.office import Office
from server.cshr.models.users import User
from server.cshr.models.vacations import PublicHoliday


def filter_public_holidays_by_month_and_year(user: User, year: str, month: str):
  """
    Filter holidays based on user location and the year and month to be displayed on the calander.
  """
  location: Office = user.location
  return PublicHoliday.objects.filter(location=location, holiday_date__year=year, holiday_date__month=month)