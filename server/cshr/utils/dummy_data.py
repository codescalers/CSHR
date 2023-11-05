from typing import List, Dict, Any
from server.cshr.models.office import WEEKEND_DAYS, Office
from server.cshr.models.users import User, TEAM, USER_TYPE, GENDER_TYPE

users: List[Dict[str, Any]] = [
  {
    "first_name": "Nayer",
    "last_name": "Admin",
    "password": "123456789",
    "email": "nayer@admin.com",
    "mobile_number": "123456789123",
    "telegram_link": "@nayer",
    "team": TEAM.BusinessDevelopment,
    "user_type": USER_TYPE.ADMIN,
    "address": "---",
    "job_title": "Manager",
    "gender" : GENDER_TYPE.MALE,
  },
  {
    "first_name": "Nayer",
    "last_name": "User",
    "password": "123456789",
    "email": "nayer@user.com",
    "mobile_number": "123456789123",
    "telegram_link": "@nayer",
    "team": TEAM.BusinessDevelopment,
    "user_type": USER_TYPE.USER,
    "address": "---",
    "job_title": "Manager",
    "gender" : GENDER_TYPE.MALE,
  },
  {
    "first_name": "Nayer",
    "last_name": "Supervisor",
    "password": "123456789",
    "email": "nayer@supervisor.com",
    "mobile_number": "123456789123",
    "telegram_link": "@nayer",
    "team": TEAM.BusinessDevelopment,
    "user_type": USER_TYPE.SUPERVISOR,
    "address": "---",
    "job_title": "Manager",
    "gender" : GENDER_TYPE.MALE,
  },
  {
    "first_name": "Rafik",
    "last_name": "Admin",
    "password": "123456789",
    "email": "rafik@admin.com",
    "mobile_number": "123456789123",
    "telegram_link": "@rafik",
    "team": TEAM.HRAndFinance,
    "user_type": USER_TYPE.ADMIN,
    "address": "---",
    "job_title": "HR",
    "gender" : GENDER_TYPE.MALE,
  },
  {
    "first_name": "Rafik",
    "last_name": "User",
    "password": "123456789",
    "email": "rafik@user.com",
    "mobile_number": "123456789123",
    "telegram_link": "@rafik",
    "team": TEAM.HRAndFinance,
    "user_type": USER_TYPE.USER,
    "address": "---",
    "job_title": "HR",
    "gender" : GENDER_TYPE.MALE,
  },
  {
    "first_name": "Rafik",
    "last_name": "Supervisor",
    "password": "123456789",
    "email": "rafik@supervisor.com",
    "mobile_number": "123456789123",
    "telegram_link": "@rafik",
    "team": TEAM.HRAndFinance,
    "user_type": USER_TYPE.SUPERVISOR,
    "address": "---",
    "job_title": "HR",
    "gender" : GENDER_TYPE.MALE,
  },
  {
    "first_name": "Evon",
    "last_name": "Admin",
    "password": "123456789",
    "email": "evon@admin.com",
    "mobile_number": "123456789123",
    "telegram_link": "@evon",
    "team": TEAM.HRAndFinance,
    "user_type": USER_TYPE.ADMIN,
    "address": "---",
    "job_title": "HR",
    "gender" : GENDER_TYPE.FEMALE,
  },
  {
    "first_name": "Evon",
    "last_name": "User",
    "password": "123456789",
    "email": "evon@user.com",
    "mobile_number": "123456789123",
    "telegram_link": "@evon",
    "team": TEAM.HRAndFinance,
    "user_type": USER_TYPE.USER,
    "address": "---",
    "job_title": "HR",
    "gender" : GENDER_TYPE.FEMALE,
  },
  {
    "first_name": "Evon",
    "last_name": "Supervisor",
    "password": "123456789",
    "email": "supervisor@user.com",
    "mobile_number": "123456789123",
    "telegram_link": "@evon",
    "team": TEAM.HRAndFinance,
    "user_type": USER_TYPE.SUPERVISOR,
    "address": "---",
    "job_title": "HR",
    "gender" : GENDER_TYPE.FEMALE,
  },
]

locations: List[Dict[str, Any]] = [
  {
    "name": "Belgium",
    "country": "Belgium",
    "weekend": WEEKEND_DAYS.Saturday_and_Sunday
  },
  {
    "name": "Egypt",
    "country": "Egypt",
    "weekend": WEEKEND_DAYS.Friday_and_Saturday
  },
  {
    "name": "India",
    "country": "India",
    "weekend": WEEKEND_DAYS.Saturday_and_Sunday
  },
  {
    "name": "Mauritius",
    "country": "Mauritius",
    "weekend": WEEKEND_DAYS.Saturday_and_Sunday
  },
  {
    "name": "UAE",
    "country": "UAE",
    "weekend": WEEKEND_DAYS.Friday_and_Saturday
  },
  {
    "name": "Zanzi",
    "country": "Zanzi",
    "weekend": WEEKEND_DAYS.Friday_and_Saturday
  },
]

def create_locations():
  for location in locations:
    Office.objects.create(
      name=location.get("name"),
      country=location.get("country"),
      weekend=location.get("weekend")
    )

def create_users():
  for user in users:
    User.objects.create(
      first_name=user.get("first_name"),
      last_name=user.get("last_name"),
      email=user.get("email"),
      password=user.get("password"),
      mobile_number=user.get("mobile_number"),
      telegram_link=user.get("telegram_link"),
      team=user.get("team"),
      user_type=user.get("user_type"),
      address=user.get("address"),
      job_title=user.get("job_title"),
      gender=user.get("gender"),
    )
  