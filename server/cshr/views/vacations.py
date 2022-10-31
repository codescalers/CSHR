from server.cshr.serializers.users import TeamSerializer
from server.cshr.serializers.vacations import (
    AdminVacationBalanceSerializer,
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
from server.cshr.models.users import User
from server.cshr.utils.vacation_balance_helper import StanderdVacationBalance
from server.cshr.services.users import get_user_by_id
from server.cshr.services.vacations import (
    get_balance_by_user,
    get_vacation_by_id,
    get_all_vacations,
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
    get_vacation_request_email_template,
    get_vacation_reply_email_template,
)
from server.cshr.celery.send_email import send_email_for_request
from server.cshr.celery.send_email import send_email_for_reply
from server.cshr.models.vacations import Vacation
from server.cshr.services.vacations import get_vacations_by_user
from server.cshr.utils.redis_functions import (
    notification_commented,
    set_notification_request_redis,
    set_notification_reply_redis,
)


class AdminVacationBalanceApiView(GenericAPIView):
    """Class VacationBalance to update or post vacation balance by only admin."""

    serializer_class = AdminVacationBalanceSerializer
    permission_classes = [IsAdmin]

    def post(self, request: Request) -> Response:
        v = StanderdVacationBalance()
        request.data["sick_leaves"] = v.file_content["sick_leaves"]
        request.data["compensation"] = v.file_content["compensation"]
        request.data["unpaid"] = v.file_content["unpaid"]
        request.data["year"] = datetime.today().year
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            for field, value in request.data.items():
                v.write(field, value)
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
        v = StanderdVacationBalance()
        if (
            request.data.get("end_date")
            and type(request.data["end_date"]) == str
            and request.data.get("from_date")
            and type(request.data["from_date"]) == str
        ):
            from_date: List[str] = request.data.get("from_date").split(
                "-"
            )  # Year, month, day
            end_date: List[str] = request.data.get("end_date").split(
                "-"
            )  # Year, month, day
            converted_from_date: datetime = datetime(
                year=int(from_date[0]), month=int(from_date[1]), day=int(from_date[2])
            ).date()
            converted_end_date: datetime = datetime(
                year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2])
            ).date()
            request.data["from_date"] = converted_from_date
            request.data["end_date"] = converted_end_date
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            saved = serializer.save(
                type=TYPE_CHOICES.VACATIONS,
                status=STATUS_CHOICES.PENDING,
                applying_user=request.user,
            )
            balance = v.check_balance(
                user=request.user,
                vacation=saved,
                reason=serializer.validated_data.get("reason"),
                start_date=serializer.validated_data.get("from_date"),
                end_date=serializer.validated_data.get("end_date"),
            )
            if balance is not True:
                return CustomResponse.bad_request(message=balance)
            msg = get_vacation_request_email_template(
                request.user, serializer.data, saved.id
            )
            set_notification_request_redis(serializer.data)
            send_email_for_request(request.user.id, msg, "Vacation request")
            return CustomResponse.success(
                status_code=201, message="Successfully Vacation Posted!"
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
            balance = v.check_balance(
                user=request.user,
                reason=serializer.validated_data.get("reason"),
                start_date=serializer.validated_data.get("from_date"),
                end_date=serializer.validated_data.get("end_date"),
                vacation=vacation,
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
                message="vacation request accepted", status_code=202
            )
        else:
            return CustomResponse.not_found(
                message="user is not found", status_code=404
            )


class VacationsRejectApiView(ListAPIView, GenericAPIView):
    permission_classes = [IsSupervisor | IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")
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
            message="Baance founded.", data=self.get_serializer(balance).data
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
        serializer = self.get_serializer(user_balance, data=request.data)
        if serializer.is_valid():
            print(user)
            if request.data.get("delete_old_balance") is True:
                serializer.save(old_balance={}, user=user)
            else:
                serializer.save(user=user)
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
        converted_from_date: datetime = datetime(
            year=int(start_date[0]), month=int(start_date[1]), day=int(start_date[2])
        ).date()
        converted_end_date: datetime = datetime(
            year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2])
        ).date()
        actual_days: int = v.remove_weekends(
            user, converted_from_date, converted_end_date
        )
        return CustomResponse.success(message="Baance founded.", data=actual_days)
