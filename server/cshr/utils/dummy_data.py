import datetime
from typing import List, Dict, Any
from server.cshr.models.office import WEEKEND_DAYS, Office
from django.contrib.auth.hashers import make_password

locations: List[Dict[str, Any]] = [
    {"name": "Egypt", "country": "Egypt", "weekend": WEEKEND_DAYS.Friday_and_Saturday},
    {
        "name": "Belgium",
        "country": "Belgium",
        "weekend": WEEKEND_DAYS.Saturday_and_Sunday,
    },
    {"name": "India", "country": "India", "weekend": WEEKEND_DAYS.Saturday_and_Sunday},
    {
        "name": "Mauritius",
        "country": "Mauritius",
        "weekend": WEEKEND_DAYS.Saturday_and_Sunday,
    },
    {"name": "UAE", "country": "UAE", "weekend": WEEKEND_DAYS.Friday_and_Saturday},
    {"name": "Zanzi", "country": "Zanzi", "weekend": WEEKEND_DAYS.Friday_and_Saturday},
]


def create_locations():
    for location in locations:
        Office.objects.create(
            name=location.get("name"),
            country=location.get("country"),
            weekend=location.get("weekend"),
        )


def create_vacation_balance():
    from server.cshr.models.vacations import OfficeVacationBalance

    for location in locations:
        OfficeVacationBalance.objects.create(
            location=Office.objects.get(
                name=location["name"],
                country=location["country"],
                weekend=location["weekend"],
            )
        )


def create_users():
    from server.cshr.models.users import User, TEAM, USER_TYPE, GENDER_TYPE

    users: List[Dict[str, Any]] = [
        {
            "first_name": "Mahmoud",
            "last_name": "Emad",
            "password": "123456789",
            "email": "mahmoud@admin.com",
            "mobile_number": "123456789123",
            "telegram_link": "@mahmoud",
            "team": TEAM.BusinessDevelopment,
            "user_type": USER_TYPE.ADMIN,
            "address": "---",
            "social_insurance_number": "---",
            "job_title": "Manager",
            "gender": GENDER_TYPE.MALE,
            "birthday": datetime.date(year=2005, month=10, day=6),
            "joining_at": datetime.date(year=2005, month=10, day=6),
        },
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
            "social_insurance_number": "---",
            "job_title": "Manager",
            "gender": GENDER_TYPE.MALE,
            "birthday": datetime.date(year=2000, month=12, day=12),
            "joining_at": datetime.date(year=2000, month=12, day=12),
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
            "social_insurance_number": "---",
            "job_title": "Manager",
            "gender": GENDER_TYPE.MALE,
            "birthday": datetime.date(year=2000, month=12, day=13),
            "joining_at": datetime.date(year=2000, month=12, day=13),
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
            "social_insurance_number": "---",
            "job_title": "Manager",
            "gender": GENDER_TYPE.MALE,
            "birthday": datetime.date(year=2000, month=9, day=17),
            "joining_at": datetime.date(year=2000, month=9, day=17),
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
            "social_insurance_number": "---",
            "job_title": "HR",
            "gender": GENDER_TYPE.MALE,
            "birthday": datetime.date(year=2000, month=1, day=12),
            "joining_at": datetime.date(year=2000, month=1, day=12),
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
            "social_insurance_number": "---",
            "job_title": "HR",
            "gender": GENDER_TYPE.MALE,
            "birthday": datetime.date(year=1998, month=4, day=15),
            "joining_at": datetime.date(year=1998, month=4, day=15),
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
            "social_insurance_number": "---",
            "job_title": "HR",
            "gender": GENDER_TYPE.MALE,
            "birthday": datetime.date(year=1959, month=2, day=22),
            "joining_at": datetime.date(year=1959, month=2, day=22),
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
            "social_insurance_number": "---",
            "job_title": "HR",
            "gender": GENDER_TYPE.FEMALE,
            "birthday": datetime.date(year=2002, month=3, day=15),
            "joining_at": datetime.date(year=2002, month=3, day=15),
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
            "social_insurance_number": "---",
            "job_title": "HR",
            "gender": GENDER_TYPE.FEMALE,
            "birthday": datetime.date(year=2000, month=12, day=12),
            "joining_at": datetime.date(year=2000, month=12, day=12),
        },
        {
            "first_name": "Evon",
            "last_name": "Supervisor",
            "password": "123456789",
            "email": "evon@supervisor.com",
            "mobile_number": "123456789123",
            "telegram_link": "@evon",
            "team": TEAM.HRAndFinance,
            "user_type": USER_TYPE.SUPERVISOR,
            "address": "---",
            "social_insurance_number": "---",
            "job_title": "HR",
            "gender": GENDER_TYPE.FEMALE,
            "birthday": datetime.date(year=2000, month=12, day=25),
            "joining_at": datetime.date(year=2000, month=12, day=25),
        },
    ]

    index = 0

    for user in users:

        if index == 6:
            index = 0

        location = Office.objects.get_or_create(
            name=locations[index].get("name"),
            country=locations[index].get("country"),
            weekend=locations[index].get("weekend"),
        )

        User.objects.create(
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            email=user.get("email"),
            password=make_password(user.get("password")),
            mobile_number=user.get("mobile_number"),
            telegram_link=user.get("telegram_link"),
            team=user.get("team"),
            user_type=user.get("user_type"),
            address=user.get("address"),
            social_insurance_number=user.get("social_insurance_number"),
            job_title=user.get("job_title"),
            gender=user.get("gender"),
            birthday=user.get("birthday"),
            joining_at=user.get("joining_at"),
            location=location[0],
        )
        index += 1
