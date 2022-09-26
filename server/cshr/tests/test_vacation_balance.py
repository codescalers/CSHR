from rest_framework.test import APITestCase
from server.cshr.models.vacations import PublicHolidays
from server.cshr.utils.vacation_balance_helper import VacationBalanceHelper
from server.cshr.models.users import User
from server.cshr.models.office import Office
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
import datetime


class VacationBalanceTest(APITestCase):
    def setUp(self):
        office = Office.objects.create(
            name="testOffice",
            country="testCountry",
            official_holidays=["Friday", "Saturday"],
        )
        u = User.objects.create(
            first_name="Ahmed",
            last_name="Mohamed",
            telegram_link="https://t.me/ahmed2",
            email="ahmed@gmail.com",
            birthday="1995-08-24",
            mobile_number="0123456789",
            password=make_password("ahmedpass"),
            location=office,
            team="Development",
            user_type="Admin",
        )

        u.created_at = date(date.today().year, 1, 1)
        u.save()
        v = VacationBalanceHelper()
        v.check(u)

    def create_user(self, month: int):
        office = Office.objects.create(
            name="CodeScalers", country="Egypt", official_holidays=["Friday"]
        )
        u = User.objects.create(
            first_name="Ahmed",
            last_name="Mohamed",
            telegram_link="https://t.me/ahmed2",
            email="ahmd@gmail.com",
            birthday="1995-08-24",
            mobile_number="012346789",
            password=make_password("ahmedpass"),
            location=office,
            team="Development",
            user_type="Admin",
        )

        u.created_at = date(date.today().year, month, month)
        u.save()
        v = VacationBalanceHelper()
        v.check(u)

    def test_empty_old_balance(self):
        """
        Old balance should be empty when the user is created
        """
        u = User.objects.get(pk=1)
        self.assertEqual(u.vacationbalance.old_balance, {})

    def test_not_empty_old_balance(self):
        u = User.objects.get(pk=1)
        v = VacationBalanceHelper()
        v.old_balance_format(u)
        self.assertNotEqual(u.vacationbalance.old_balance, {})

    def test_write_to_balance_file(self):
        """
        make sure the file is updated when the write function called.
        That will run every year
        """
        content = {
            "annual_leaves": 15,
            "sick_leaves": 100,
            "compensation": 0,
            "unpaid": 0,
            "emergencies": 4,
            "leave_execuses": 5,
            "public_holidays": ["2022-10-12", "2022-10-14", "2022-10-13"],
            "year": 2022,
        }

        v = VacationBalanceHelper()
        v.bulk_write(content)
        self.assertEqual(v.file_content["annual_leaves"], 15)
        self.assertEqual(len(v.file_content["public_holidays"]), 3)

    def test_user_balance(self):
        u = User.objects.get(pk=1)
        content = {
            "annual_leaves": 15,
            "sick_leaves": 100,
            "compensation": 0,
            "unpaid": 0,
            "emergencies": 4,
            "leave_execuses": 5,
            "public_holidays": ["2022-10-12", "2022-10-14", "2022-10-13"],
            "year": 2022,
        }

        v = VacationBalanceHelper()
        v.bulk_write(content)
        self.assertEqual(u.vacationbalance.public_holidays, 3)
        self.assertEqual(u.vacationbalance.annual_leaves, 15)
        self.assertEqual(u.vacationbalance.emergencies, 4)

    def test_public_holidays_count(self):
        v = VacationBalanceHelper()
        public_holidays = ["2022-09-30"]
        v.write("public_holidays", public_holidays)
        public_holidays = v.read_file()["public_holidays"]
        u = User.objects.get(pk=1)
        count = v.calculate_public_holidays(
            public_holidays=public_holidays, created_at=u.created_at
        )
        self.assertEqual(count, 4)

    def test_reset_old_balance(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        v.old_balance_format(u)
        v.resetting_old_balance(u)
        self.assertEqual(u.vacationbalance.old_balance, {})

    def test_check_old_balance(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        res = v.check_old_balance(u, "annual_leaves")
        self.assertEqual(res, 0)
        wanted = u.vacationbalance.annual_leaves
        v.old_balance_format(u)
        res = v.check_old_balance(u, "annual_leaves")
        self.assertEqual(res, wanted)

    def test_update_old_balance(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        v.old_balance_format(u)
        v.update_json_format(u.vacationbalance, "annual_leaves", 5)
        self.assertEqual(u.vacationbalance.old_balance["annual_leaves"], 5)

    def test_calculate_vacation_values(self):
        content = {
            "annual_leaves": 15,
            "sick_leaves": 100,
            "compensation": 0,
            "unpaid": 0,
            "emergencies": 4,
            "leave_execuses": 5,
            "public_holidays": ["2022-10-10", "2022-10-24", "2022-10-23"],
            "year": 2022,
        }
        v = VacationBalanceHelper()
        v.bulk_write(content)
        u = User.objects.get(pk=1)
        v.calculate_vacation_values(u.created_at)
        self.assertEqual(u.vacationbalance.annual_leaves, 15)

    def test_registered_user_at_may(self):
        # assuming the annual_leaves balance is 15 so per month 1.25 days
        # so if the user joined at jan it will be 12 * 1.25 wich is full balance
        # if the user joined at may then it will be 8 * 1.25 and so on
        balance = {
            "annual_leaves": 15,
            "sick_leaves": 100,
            "compensation": 0,
            "unpaid": 0,
            "emergencies": 4,
            "leave_execuses": 5,
            "public_holidays": ["2022-10-12", "2022-10-14", "2022-10-13"],
            "year": 2022,
        }
        v = VacationBalanceHelper()
        v.bulk_write(balance)
        self.create_user(5)
        u = User.objects.get(pk=2)
        self.assertEqual(u.vacationbalance.annual_leaves, 10)
        self.assertEqual(u.vacationbalance.emergencies, 3)
        self.assertEqual(u.vacationbalance.leave_execuses, 3)

    def test_check_balance(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        # including today and bearing in mind that user's total balance of annual leaves is 15
        # this should pass
        res = v.check_balance(
            u,
            "annual_leaves",
            datetime.datetime.now(),
            datetime.datetime.now() + timedelta(13),
        )
        self.assertEqual(res, True)
        # but in this case including today and another 15 days so it exceeded the current balance
        res = v.check_balance(
            u,
            "annual_leaves",
            datetime.datetime.now(),
            datetime.datetime.now() + timedelta(15),
        )
        self.assertEqual(res, "You only have 15 days left of type annual_leaves")

    def test_check_balance_while_having_old_balance(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        # this will make the user's old balance of annual leaves 15,
        # which is equivelant to his current annual leaves
        v.old_balance_format(u)
        # the user's total balance now is 30 so the request is valid
        res = v.check_balance(
            u,
            "annual_leaves",
            datetime.datetime.now(),
            datetime.datetime.now() + timedelta(28),
        )
        self.assertEqual(res, True)
        res = v.check_balance(
            u,
            "annual_leaves",
            datetime.datetime.now(),
            datetime.datetime.now() + timedelta(31),
        )
        self.assertEqual(res, "You only have 30 days left of type annual_leaves")

    def test_apply_for_vacation_with_invalid_input(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        res = v.apply_for_vacation(
            u,
            datetime.datetime.now(),
            datetime.datetime.now() + timedelta(-3),
            "annual_leaves",
        )
        self.assertEqual(res, "Invalid Input")

    def test_apply_for_vacation_while_having_balance(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        PublicHolidays.objects.create(date=datetime.datetime.now())
        res = v.apply_for_vacation(
            u,
            datetime.datetime.now(),
            datetime.datetime.now() + timedelta(2),
            "annual_leaves",
        )
        self.assertEqual(res, 13)

    def test_apply_for_vacation_while_having_old_balance(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        v.old_balance_format(u)
        PublicHolidays.objects.create(date=datetime.datetime.now() + timedelta(1))
        res = v.apply_for_vacation(
            u,
            datetime.datetime.now(),
            datetime.datetime.now() + timedelta(2),
            "annual_leaves",
        )
        self.assertEqual(res, 13)
        self.assertEqual(u.vacationbalance.annual_leaves, 15)

    def test_apply_for_vacation_with_public_and_official_holidays(self):
        v = VacationBalanceHelper()
        u = User.objects.get(pk=1)
        v.old_balance_format(u)
        base_old_balance = u.vacationbalance.old_balance["annual_leaves"]
        PublicHolidays.objects.create(date=datetime.datetime.now().date())
        today = datetime.datetime.now().today()
        friday = today + timedelta(((4 - today.weekday()) % 7))
        want = v.get_difference_between_two_days(today, friday)
        res = v.calculate_public_and_official_holidays(u, today, want)
        if want == 0:
            expected = 1
        else:
            expected = 2
        self.assertEqual(res, expected)
        exp = want - expected
        if want == 0:
            exp = want
        res = v.apply_for_vacation(u, today, friday, "annual_leaves")
        self.assertEqual(base_old_balance - res, exp)
        self.assertEqual(u.vacationbalance.annual_leaves, 15)
