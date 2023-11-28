from server.cshr.serializers.users import TeamSerializer
from server.cshr.serializers.vacations import (
    PostOfficeVacationBalanceSerializer,
    GetOfficeVacationBalanceSerializer,
    CalculateBalanceSerializer,
    LandingPageVacationsSerializer,
    VacationsCommentsSerializer,
    VacationsSerializer,
)
from typing import Dict, List
from server.cshr.serializers.vacations import (
    VacationsUpdateSerializer,
    VacationBalanceSerializer,
    UserBalanceUpdateSerializer,
)
from server.cshr.api.permission import (
    IsSupervisor,
    IsUser,
    UserIsAuthenticated,
    IsAdmin,
)
from server.cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from server.cshr.models.users import USER_TYPE, User
from server.cshr.utils.vacation_balance_helper import StanderdVacationBalance
from server.cshr.services.users import get_user_by_id
from server.cshr.services.vacations import (
    get_balance_by_user,
    get_vacation_by_id,
    get_all_vacations,
    send_vacation_to_calendar,
    update_user_actual_balance,
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.api.response import CustomResponse
from datetime import datetime
from server.cshr.utils.update_change_log import (
    update_vacation_change_log,
)
from server.cshr.utils.email_messages_templates import (
    # get_vacation_request_email_template,
    get_vacation_reply_email_template,
)

# from server.cshr.celery.send_email import send_email_for_request
from server.cshr.celery.send_email import send_email_for_reply
from server.cshr.models.vacations import OfficeVacationBalance, PublicHoliday, Vacation
from server.cshr.services.vacations import get_vacations_by_user
from server.cshr.utils.redis_functions import (
    notification_commented,
    set_notification_request_redis,
    set_notification_reply_redis,
)


class GetAdminVacationBalanceApiView(GenericAPIView):
    """Class VacationBalance to update or post vacation balance by only admin."""

    serializer_class = GetOfficeVacationBalanceSerializer
    permission_classes = [IsAdmin]

    def get(self, request: Request) -> Response:
        year = year = datetime.now().year
        location = request.user.location
        data = OfficeVacationBalance.objects.get_or_create(year=year, location=location)

        return CustomResponse.success(
            message="Successfully updated balance values.",
            data=self.serializer_class(data[0]).data,
        )


class PostAdminVacationBalanceApiView(GenericAPIView):
    """Class VacationBalance to update or post vacation balance by only admin."""

    serializer_class = PostOfficeVacationBalanceSerializer
    permission_classes = [IsAdmin]

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        year = year = datetime.now().year
        location = request.user.location

        if serializer.is_valid():
            balance = OfficeVacationBalance.objects.filter(year=year, location=location)
            public_holidays = request.data["public_holidays"]
            for holiday in public_holidays:
                PublicHoliday.objects.get_or_create(
                    location=location, holiday_date=holiday
                )

            public_holidays = PublicHoliday.objects.filter(
                location=location, holiday_date__in=public_holidays
            ).values_list("id", flat=True)

            if len(balance) > 0:
                balance[0].annual_leaves = serializer.validated_data.get(
                    "annual_leaves"
                )
                balance[0].leave_excuses = serializer.validated_data.get(
                    "leave_excuses"
                )
                balance[0].emergency_leaves = serializer.validated_data.get(
                    "emergency_leaves"
                )
                balance[0].public_holidays.set(public_holidays)
                balance[0].save()
            else:
                serializer.save(
                    location=location, year=year, public_holidays=public_holidays[0]
                )
            return CustomResponse.success(
                message="Successfully updated balance values.", data=serializer.data
            )

        return CustomResponse.bad_request(
            message="Invalid balance values.", error=serializer.errors
        )


class BaseVacationsApiView(ListAPIView, GenericAPIView):
    """Class Vacations_APIView to create a new vacation into database or get all"""

    serializer_class = VacationsSerializer
    permission_classes = [UserIsAuthenticated]

    def post(self, request: Request) -> Response:
        """Method to create a new vacation request"""
        if (
            request.data.get("end_date")
            and type(request.data["end_date"]) == str
            and request.data.get("from_date")
            and type(request.data["from_date"]) == str
        ):
            start_date: List[str] = request.data.get("from_date").split(
                "-"
            )  # Year, month, day

            end_date: List[str] = request.data.get("end_date").split(
                "-"
            )  # Year, month, day

            try:
                converted_start_date: datetime = datetime(
                    year=int(start_date[0]),
                    month=int(start_date[1]),
                    day=int(start_date[2]),
                ).date()
            except Exception:
                return CustomResponse.bad_request(
                    message="Invalid start date format, it must match the following pattern 'yyyy-mm-dd'.",
                    error=start_date,
                )

            try:
                converted_end_date: datetime = datetime(
                    year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2])
                ).date()
            except Exception:
                return CustomResponse.bad_request(
                    message="Invalid end date format, it must match the following pattern 'yyyy-mm-dd'.",
                    error=start_date,
                )

            # Check if end date is lower than start date
            if converted_end_date < converted_start_date:
                return CustomResponse.bad_request(
                    message="The end date must be later than the start date."
                )

            request.data["from_date"] = converted_start_date
            request.data["end_date"] = converted_end_date
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            saved = serializer.save(
                type=TYPE_CHOICES.VACATIONS,
                status=STATUS_CHOICES.PENDING,
                applying_user=request.user,
            )
            # get_vacation_request_email_template(
            #     request.user, serializer.data, saved.id
            # )

            set_notification_request_redis(serializer.data)

            # send_email_for_request(request.user.id, msg, "Vacation request")
            # if not sent:
            #     return CustomResponse.bad_request(message="Error in sending email, can not sent email with this request.")
            response_date: Dict = send_vacation_to_calendar(saved)
            return CustomResponse.success(
                status_code=201,
                message="The vacation has been posted successfully.",
                data=response_date,
            )
        return CustomResponse.bad_request(error=serializer.errors)

    def get_queryset(self) -> Response:
        """method to get all vacations"""
        query_set: List[Vacation] = get_all_vacations()
        return query_set


class VacationsHelpersApiView(ListAPIView, GenericAPIView):
    serializer_class = LandingPageVacationsSerializer
    permission_classes = [UserIsAuthenticated]
    """Class Vacations_APIView to delete  vacation from database or get certain vacation"""

    def get(self, request: Request, id: str, format=None) -> Response:
        """method to get a single vacation by id"""
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(
                message="vacation is not found", status_code=404
            )

        serializer = LandingPageVacationsSerializer(vacation)
        return CustomResponse.success(
            data=serializer.data, message="vacation request found", status_code=200
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a vacation request by id"""
        vacation = get_vacation_by_id(id=id)
        if vacation is not None:
            vacation.delete()
            return CustomResponse.success(message="Hr Letter deleted", status_code=204)
        return CustomResponse.not_found(message="Hr Letter not found", status_code=404)


class VacationUserApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsUpdateSerializer
    permission_classes = [UserIsAuthenticated]

    def get(self, request: Request) -> Response:
        """method to get all vacations for certain user"""
        current_user: User = get_user_by_id(request.user.id)
        if current_user is None:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )
        vacations = get_vacations_by_user(current_user.id)
        serializer = VacationsSerializer(vacations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="vacation requests found", status_code=200
        )


class VacationsUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationsUpdateSerializer
    permission_classes = [IsUser | IsSupervisor]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        v = StanderdVacationBalance()
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")
        serializer = self.get_serializer(vacation, data=request.data, partial=True)

        if serializer.is_valid():
            balance = v.check_and_update_balance(
                applying_user=request.user,
                vacation=vacation,
                reason=serializer.validated_data.get("reason"),
                start_date=serializer.validated_data.get("from_date"),
                end_date=serializer.validated_data.get("end_date"),
            )
            if balance is not True:
                return CustomResponse.bad_request(message=balance)
            v.vacation_update_balance(vacation)
            serializer.save()
            comment: Dict = {
                "update": True,
                "user": TeamSerializer(request.user).data,
                "comment": f"{request.user.first_name.title()} update his vacation",
                "commented_at": f"{datetime.now().date()} | {datetime.now().hour}:{datetime.now().minute}",
            }
            update_vacation_change_log(vacation, comment)
            return CustomResponse.success(
                data=serializer.data,
                message="Vacation Request Updated",
                status_code=202,
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Vacation Failed to Update"
        )


class VacationsAcceptApiView(GenericAPIView):
    permission_classes = [IsSupervisor | IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")

        office_admin = (
            request.user.user_type == USER_TYPE.ADMIN
            and request.user.location == vacation.applying_user.location
        )

        if not office_admin:
            is_reporting_to = request.user in vacation.applying_user.reporting_to.all()
            if not is_reporting_to:
                return CustomResponse.unauthorized(
                    message=(
                        "You don't have the necessary permissions to perform this action. "
                        "Only supervisors and administrators working in the same office are authorized to do so."
                    )
                )

        v = StanderdVacationBalance()
        balance = v.check_and_update_balance(
            applying_user=vacation.applying_user,
            vacation=vacation,
            reason=vacation.reason,
            start_date=vacation.from_date,
            end_date=vacation.end_date,
        )

        if balance is not True:
            return CustomResponse.bad_request(message=balance)

        current_user: User = get_user_by_id(request.user.id)
        vacation.approval_user = current_user
        vacation.status = STATUS_CHOICES.APPROVED

        comment: Dict = {
            "user": TeamSerializer(request.user).data,
            "comment": f"{request.user.first_name} approved your vacation",
            "commented_at": f"{datetime.now().date()} | {datetime.now().hour}:{datetime.now().minute}",
        }

        update_vacation_change_log(vacation, comment)

        vacation.save()
        event_id = id
        bool1 = set_notification_reply_redis(vacation, "accepted", event_id)
        msg = get_vacation_reply_email_template(current_user, vacation, event_id)
        bool2 = send_email_for_reply.delay(
            current_user.id, vacation.applying_user.id, msg, "Vacation reply"
        )
        if bool1 and bool2:
            return CustomResponse.success(
                message="Vacation request accepted", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="User is not found", status_code=404
            )


class VacationsRejectApiView(ListAPIView, GenericAPIView):
    permission_classes = [IsSupervisor | IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")

        office_admin = (
            request.user.user_type == USER_TYPE.ADMIN
            and request.user.location == vacation.applying_user.location
        )

        if not office_admin:
            is_reporting_to = request.user in vacation.applying_user.reporting_to.all()
            if not is_reporting_to:
                return CustomResponse.unauthorized(
                    message=(
                        "You don't have the necessary permissions to perform this action. "
                        "Only supervisors and administrators working in the same office are authorized to do so."
                    )
                )

        if vacation.status != STATUS_CHOICES.PENDING:
            return CustomResponse.bad_request(
                message=f"The vacation status is not pinding, it's {vacation.status}."
            )

        current_user: User = get_user_by_id(request.user.id)
        vacation.approval_user = current_user
        vacation.status = STATUS_CHOICES.REJECTED

        comment: Dict = {
            "user": TeamSerializer(request.user).data,
            "comment": f"{request.user.first_name} rejacted your request",
            "commented_at": f"{datetime.now().date()} | {datetime.now().hour}:{datetime.now().minute}",
        }

        update_vacation_change_log(vacation, comment)
        vacation.save()

        event_id = id
        bool1 = set_notification_reply_redis(vacation, "rejected", event_id)
        msg = get_vacation_reply_email_template(current_user, vacation, event_id)
        bool2 = send_email_for_reply.delay(
            current_user.id, vacation.applying_user.id, msg, "Vacation reply"
        )

        if bool1 and bool2:
            return CustomResponse.success(
                message="vacation request rejected", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class VacationCommentsAPIView(GenericAPIView):
    """Use this endpoint to add a comment as a user."""

    permission_classes = [UserIsAuthenticated]
    serializer_class = VacationsCommentsSerializer

    def put(self, request: Request, id: str) -> Request:
        """Use this endpoint to approve request."""
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.bad_request(status_code=404)
        comment: Dict = {
            "user": TeamSerializer(request.user).data,
            "comment": request.data.get("comment"),
            "commented_at": f"{datetime.now().date()} | {datetime.now().hour}:{datetime.now().minute}",
        }
        update_vacation_change_log(vacation, comment)
        notification_commented(vacation, request.user, "commented", id)
        return CustomResponse.success(
            data=comment, status_code=202, message="vacation comment added"
        )


class UserVacationBalanceUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = VacationBalanceSerializer
    permission_classes = [IsAdmin]

    def put(self, request: Request):
        yourdata = request.data
        serializer = VacationBalanceSerializer(data=yourdata)
        if serializer.is_valid():
            v = StanderdVacationBalance()
            v.bulk_write(dict(serializer.data))
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="base balance updated"
            )
        return CustomResponse.bad_request(
            data=serializer.error, message="failed to update base balance"
        )


class UserBalanceUpdateApiView(ListAPIView, GenericAPIView):
    serializer_class = UserBalanceUpdateSerializer
    permission_classes = [IsAdmin]

    def put(self, request: Request):
        yourdata = request.data
        serializer = UserBalanceUpdateSerializer(data=yourdata)
        if serializer.is_valid():
            vh = StanderdVacationBalance()
            ids = serializer.data["ids"]
            type = serializer.data["type"]
            new_value = serializer.data["new_value"]
            for id in ids:
                try:
                    u = get_user_by_id(id=int(id))
                except User.DoesNotExist:
                    return CustomResponse.bad_request(
                        data=serializer.error, message="failed to update balance"
                    )
                vh.check(u)
                v = u.vacationbalance
                vh.update_balance(type, v, new_value)
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="Users' balance updated"
            )
        return CustomResponse.bad_request(
            data=serializer.error, message="failed to update balance"
        )


class UserVacationBalanceApiView(GenericAPIView):
    serializer_class = VacationBalanceSerializer
    permission_classes = [
        UserIsAuthenticated,
    ]

    def get(self, request: Request) -> Response:
        """Get method to get all user balance"""
        user_id = request.query_params.get("user_id")

        if not user_id.isdigit():
            return CustomResponse.bad_request(message="Invalid user id.")

        if user_id is None:
            return CustomResponse.bad_request(
                message="You must send `user_id` as a query_params."
            )

        user: User = get_user_by_id(user_id)

        if user is None:
            return CustomResponse.not_found(message="User not found.")

        v: StanderdVacationBalance = StanderdVacationBalance()

        balance = v.check(user)
        request.data["user"] = TeamSerializer(user).data

        return CustomResponse.success(
            message="Sucess found balance.",
            data=CalculateBalanceSerializer(balance).data,
        )

    def put(self, request: Request) -> CustomResponse:
        """Use this endpoint to update user balance"""
        user_id = request.query_params.get("user_id")
        if not user_id.isdigit():
            return CustomResponse.bad_request(message="Invalid user id.")
        if user_id is None:
            return CustomResponse.bad_request(
                message="You must send `user_id` as a query_params."
            )
        user: User = get_user_by_id(user_id)
        v: StanderdVacationBalance = StanderdVacationBalance()
        v.check(user)
        user_balance = get_balance_by_user(user)

        # Set default values
        request.data["compensation"] = 365
        request.data["sick_leaves"] = 365
        request.data["unpaid"] = 365

        serializer = self.get_serializer(user_balance, data=request.data)

        if serializer.is_valid():
            # if request.data.get("delete_old_balance") is True:
            #     serializer.save(old_balance={}, user=user)
            # else:
            serializer.save(user=user)
            update_user_actual_balance(user_balance)
            return CustomResponse.success(
                message="Successfully updated user balance",
                status_code=202,
                data=serializer.data,
            )
        return CustomResponse.bad_request(
            message="Please make sure that you entered a valid data",
            error=serializer.errors,
        )


class CalculateVacationDaysApiView(GenericAPIView):
    permission_classes = [
        UserIsAuthenticated,
    ]

    def get(self, request: Request) -> Response:
        """Use this endpoint to calculate the actual vacation days taked between 2 dates."""
        user: User = get_user_by_id(request.user.id)
        v: StanderdVacationBalance = StanderdVacationBalance()
        v.check(user)

        start_date: List[str] = request.query_params.get("start_date").split("-")
        end_date: List[str] = request.query_params.get("end_date").split("-")

        try:
            converted_start_date: datetime = datetime(
                year=int(start_date[0]),
                month=int(start_date[1]),
                day=int(start_date[2]),
            ).date()
        except Exception:
            return CustomResponse.bad_request(
                message="Invalid start date format, it must match the following pattern 'yyyy-mm-dd'.",
                error=start_date,
            )

        try:
            converted_end_date: datetime = datetime(
                year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2])
            ).date()
        except Exception:
            return CustomResponse.bad_request(
                message="Invalid end date format, it must match the following pattern 'yyyy-mm-dd'.",
                error=end_date,
            )

        actual_days: int = v.remove_weekends(
            user, converted_start_date, converted_end_date
        )
        actual_days: int = v.remove_holidays(
            user, converted_start_date, converted_end_date, actual_days
        )

        # actual_days = len(actual_days) if actual_days != None else 0
        return CustomResponse.success(message="Balance calculated.", data=actual_days)
