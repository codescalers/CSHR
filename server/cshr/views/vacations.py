from cshr.serializers.users import TeamSerializer
from cshr.serializers.vacations import (
    AdminApplyVacationForUserSerializer,
    PostOfficeVacationBalanceSerializer,
    GetOfficeVacationBalanceSerializer,
    CalculateBalanceSerializer,
    LandingPageVacationsSerializer,
    VacationBalanceAdjustmentSerializer,
    VacationsCommentsSerializer,
    VacationsSerializer,
)
from typing import Dict, List
from cshr.serializers.vacations import (
    VacationsUpdateSerializer,
    VacationBalanceSerializer,
    UserBalanceUpdateSerializer,
)
from cshr.api.permission import (
    IsSupervisor,
    IsUser,
    UserIsAuthenticated,
    IsAdmin,
)
from cshr.models.requests import TYPE_CHOICES, STATUS_CHOICES
from cshr.models.users import USER_TYPE, User
from cshr.services.office import get_office_by_id
from cshr.utils.vacation_balance_helper import StanderdVacationBalance
from cshr.services.users import (
    build_user_reporting_to_hierarchy,
    get_user_by_id,
    get_users_by_id,
)
from cshr.services.vacations import (
    filter_balances_by_users,
    get_vacation_by_id,
    get_all_vacations,
)
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from cshr.api.response import CustomResponse
from datetime import datetime, timedelta
from cshr.utils.update_change_log import (
    update_vacation_change_log,
)
from cshr.utils.email_messages_templates import (
    # get_vacation_request_email_template,
    get_vacation_reply_email_template,
)

# from cshr.celery.send_email import send_email_for_request
from cshr.celery.send_email import send_email_for_reply
from cshr.models.vacations import (
    REASON_CHOICES,
    OfficeVacationBalance,
    PublicHoliday,
    Vacation,
)
from cshr.services.vacations import get_vacations_by_user
from cshr.utils.redis_functions import (
    http_ensure_redis_error,
    notification_commented,
    ping_redis,
    set_notification_request_redis,
    set_notification_reply_redis,
)
from cshr.utils.wrappers import wrap_vacation_request
from cshr.services.notifications import NotificationsService


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


class VacationBalanceAdjustmentApiView(GenericAPIView):
    """Class VacationBalanceAdjustmentApiView to update or vacation <reason> balance by only admin to the whole office."""

    serializer_class = VacationBalanceAdjustmentSerializer
    permission_classes = [IsAdmin]

    def put(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            office_id = serializer.validated_data.get("officeId")
            office = get_office_by_id(office_id)
            if not office:
                return CustomResponse.not_found(message="Office not found.")

            users_in_office = User.objects.filter(location=office)

            # Check the balance if created for all users
            v: StanderdVacationBalance = StanderdVacationBalance()
            for user in users_in_office:
                v.check(user)

            return CustomResponse.success(
                message="Successfully updated balance values.",
                data=serializer.data,
            )

        return CustomResponse.bad_request(
            message="Please make sure that you entred a valid data."
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

            if len(public_holidays) <= len(balance[0].public_holidays.all()):
                deleted_holidays = []
                for holiday in balance[0].public_holidays.all():
                    if holiday.id not in public_holidays:
                        deleted_holidays.append(holiday)

                for day in deleted_holidays:
                    PublicHoliday.objects.get(id=day.id).delete()

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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.get("from_date")
            end_date = serializer.validated_data.get("end_date")
            applying_user = request.user

            # Check if there are pending vacations in the same day.
            date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
            for date in date_range:
                pending_requests = Vacation.objects.filter(
                    from_date__lte=date,
                    end_date__gte=date,
                    status=STATUS_CHOICES.PENDING,
                    applying_user=applying_user,
                )
            if len(pending_requests) > 0:
                return CustomResponse.bad_request(
                    message="You have a request with a pending status on the same day. Kindly address the pending requests first by either deleting them or reaching out to the administrators for approval/rejection."
                )

            # Check balance.
            v = StanderdVacationBalance()
            v.check(applying_user)

            reason: str = serializer.validated_data.get("reason")
            user_reason_balance = applying_user.vacationbalance

            vacation_days = v.get_actual_days(applying_user, start_date, end_date)

            if start_date.day == end_date.day:
                # The request is the same day
                start_hour = start_date.hour
                end_hour = end_date.hour
                times = v.calculate_times(start_hour=start_hour, end_hour=end_hour)
                if times < 1:
                    if not v.is_valid_times(
                        times=times, start_hour=start_hour, end_hour=end_hour
                    ):
                        return CustomResponse.bad_request(
                            message=f"You've sent an invalid times, The days should match the {times}"
                        )
                    vacation_days = times

            if reason == REASON_CHOICES.PUBLIC_HOLIDAYS:
                return CustomResponse.bad_request(
                    message=f"You have sent an invalid reason {reason}",
                    error={
                        "message": "This field should be one of the follwing reasons",
                        "reasons": [
                            reason
                            for reason in REASON_CHOICES
                            if reason != REASON_CHOICES.PUBLIC_HOLIDAYS
                        ],
                    },
                )
            else:
                curr_balance = getattr(user_reason_balance, reason)

                if curr_balance < vacation_days:
                    return CustomResponse.bad_request(
                        message=f"You only have {curr_balance} days left of reason '{reason.capitalize().replace('_', ' ')}'"
                    )

                pending_vacations = Vacation.objects.filter(
                    status=STATUS_CHOICES.PENDING,
                    applying_user=applying_user,
                    reason=reason,
                ).values_list("actual_days", flat=True)

                chcked_balance = curr_balance - sum(pending_vacations)

                if chcked_balance < vacation_days:
                    return CustomResponse.bad_request(
                        message=f"You have an additional pending request that deducts {sum(pending_vacations)} days from your balance even though the current balance for the '{reason.capitalize().replace('_', ' ')}' category is only {curr_balance} days."
                    )

                vacation = serializer.save(
                    type=TYPE_CHOICES.VACATIONS,
                    status=STATUS_CHOICES.PENDING,
                    applying_user=applying_user,
                    actual_days=vacation_days,
                )

                # msg = get_vacation_request_email_template(
                #     request.user, serializer.data, vacation.id
                # )

                # try:
                #     ping_redis()
                # except:
                #     return http_ensure_redis_error()

                # receivers = build_user_reporting_to_hierarchy(applying_user)
                # receivers = User.objects.filter(id__in = receivers)

                # notification = NotificationsService(sender=applying_user, receivers=receivers)
                # message = notification.vacations.post_new_vacation(reason_format)
                # notification.push(message)

                # notification.push()

                # set_notification_request_redis(serializer.data)

                # sent = send_email_for_request(request.user.id, msg, "Vacation request")
                # if not sent:
                #     return CustomResponse.bad_request(message="Error in sending email, can not sent email with this request.")

                vacation_data: Dict = wrap_vacation_request(vacation)
                return CustomResponse.success(
                    status_code=201,
                    message="The vacation has been posted successfully.",
                    data=vacation_data,
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
            if vacation.status == STATUS_CHOICES.APPROVED:
                v = StanderdVacationBalance()
                balance = v.check_and_update_balance(
                    applying_user=vacation.applying_user,
                    vacation=vacation,
                    reason=vacation.reason,
                    start_date=vacation.from_date,
                    end_date=vacation.end_date,
                    delete=True,
                )
                if balance is not True:
                    return CustomResponse.bad_request(message=balance)

            vacation.delete()
            return CustomResponse.success(
                message="The vacation has been deleted successfully.", status_code=204
            )
        return CustomResponse.not_found(
            message="The vacation is not found.", status_code=404
        )


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
    permission_classes = [IsUser | IsSupervisor | IsAdmin]

    def put(self, request: Request, id: str, format=None) -> Response:
        vacation = get_vacation_by_id(id=id)
        v = StanderdVacationBalance()
        if vacation is None:
            return CustomResponse.not_found(message="Vacation not found")
        serializer = self.get_serializer(vacation, data=request.data, partial=True)

        if serializer.is_valid():
            start_date = serializer.validated_data.get("from_date")
            end_date = serializer.validated_data.get("end_date")

            # Check if there are pending vacations in the same day
            date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
            for date in date_range:
                pending_requests = Vacation.objects.filter(
                    from_date__lte=date,
                    end_date__gte=date,
                    status=STATUS_CHOICES.PENDING,
                )
            if len(pending_requests) > 0:
                return CustomResponse.bad_request(
                    message="You have a request with a pending status on the same day. Kindly address the pending requests first by either deleting them or reaching out to the administrators for approval/rejection."
                )

            # Check balance.
            v = StanderdVacationBalance()
            reason: str = serializer.validated_data.get("reason")
            applying_user = request.user
            user_reason_balance = applying_user.vacationbalance
            vacation_days = v.get_actual_days(applying_user, start_date, end_date)

            curr_balance = getattr(user_reason_balance, reason)

            pending_vacations = Vacation.objects.filter(
                status=STATUS_CHOICES.PENDING,
                applying_user=applying_user,
                reason=reason,
            ).values_list("actual_days", flat=True)

            chcked_balance = curr_balance - sum(pending_vacations)

            if curr_balance < vacation_days:
                return CustomResponse.bad_request(
                    message=f"You only have {curr_balance} days left of reason '{reason.capitalize().replace('_', ' ')}'"
                )

            if chcked_balance < vacation_days:
                return CustomResponse.bad_request(
                    message=f"You have an additional pending request that deducts {sum(pending_vacations)} days from your balance even though the current balance for the '{reason.capitalize().replace('_', ' ')}' category is only {curr_balance} days."
                )

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
            leaders = build_user_reporting_to_hierarchy(vacation.applying_user)
            is_reporting_to = request.user.id in leaders
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
        try:
            ping_redis()
        except:
            return http_ensure_redis_error()

        bool1 = set_notification_reply_redis(vacation, "accepted", event_id)
        msg = get_vacation_reply_email_template(current_user, vacation, event_id)
        bool2 = send_email_for_reply.delay(
            current_user.id, vacation.applying_user.id, msg, "Vacation reply"
        )

        if bool1 and bool2:
            return CustomResponse.success(
                message="Vacation request accepted",
                status_code=202,
                data=VacationsUpdateSerializer(vacation).data,
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
            leaders = build_user_reporting_to_hierarchy(vacation.applying_user)
            is_reporting_to = request.user.id in leaders
            if not is_reporting_to:
                return CustomResponse.unauthorized(
                    message=(
                        "You don't have the necessary permissions to perform this action. "
                        "Only supervisors and administrators working in the same office are authorized to do so."
                    )
                )

        if vacation.status != STATUS_CHOICES.PENDING:
            return CustomResponse.bad_request(
                message=f"The vacation status is not pending, it's {vacation.status}."
            )

        current_user: User = get_user_by_id(request.user.id)
        vacation.approval_user = current_user
        vacation.status = STATUS_CHOICES.REJECTED

        comment: Dict = {
            "user": TeamSerializer(request.user).data,
            "comment": f"{request.user.first_name} rejected your request",
            "commented_at": f"{datetime.now().date()} | {datetime.now().hour}:{datetime.now().minute}",
        }

        update_vacation_change_log(vacation, comment)
        vacation.save()

        event_id = id

        try:
            ping_redis()
        except:
            return http_ensure_redis_error()

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

        try:
            ping_redis()
        except:
            return http_ensure_redis_error()

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
        user_ids = request.query_params.get("user_ids")
        if user_ids is None:
            return CustomResponse.bad_request(
                message="You must send `user_ids` as a query_params."
            )

        user_ids = user_ids.split(",")
        users: User = get_users_by_id(user_ids)

        v: StanderdVacationBalance = StanderdVacationBalance()
        balances = []

        for user in users:
            balance = v.check(user)
            balances.append(balance)

        request.data["user"] = TeamSerializer(user).data
        return CustomResponse.success(
            message="Sucess found balance.",
            data=CalculateBalanceSerializer(balances, many=True).data,
        )

    def put(self, request: Request) -> CustomResponse:
        """Use this endpoint to update user balance"""

        user_ids = request.query_params.get("user_ids")
        if user_ids is None:
            return CustomResponse.bad_request(
                message="You must send `user_id` as a query_params."
            )

        user_ids = user_ids.split(",")
        users: User = get_users_by_id(user_ids)

        v: StanderdVacationBalance = StanderdVacationBalance()

        balances = filter_balances_by_users(users)

        # Set default values
        request.data["sick_leaves"] = 365
        request.data["unpaid"] = 365

        try:
            for balance in balances:
                balance.sick_leaves = 365
                balance.unpaid = 365
                balance.annual_leaves = int(request.data.get("annual_leaves"))
                balance.emergency_leaves = int(request.data.get("emergency_leaves"))
                balance.leave_excuses = int(request.data.get("leave_excuses"))
                balance.compensation = int(request.data.get("compensation"))
                balance.save()

                v.check(balance.user)

            return CustomResponse.success(
                message="Successfully updated user balance",
                status_code=202,
                data=CalculateBalanceSerializer(balances, many=True).data,
            )
            # if request.data.get("delete_old_balance") is True:
            #     serializer.save(old_balance={}, user=user)
            # else:

        except Exception:
            return CustomResponse.bad_request(
                message="Please make sure that you entered a valid data",
                status_code=400,
            )


class CalculateVacationDaysApiView(GenericAPIView):
    permission_classes = [
        UserIsAuthenticated,
    ]

    def parse_date(self, date_str: str) -> datetime:
        """Parses a date string in 'yyyy-mm-dd' format to a datetime.date object."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(
                f"Invalid date format for {date_str}, must be 'yyyy-mm-dd'."
            )

    def get(self, request: Request) -> Response:
        """Use this endpoint to calculate the actual vacation days taken between 2 dates."""
        user: User = get_user_by_id(request.user.id)
        v: StanderdVacationBalance = StanderdVacationBalance()
        v.check(user)

        start_date_str: str = request.query_params.get("start_date")
        end_date_str: str = request.query_params.get("end_date")

        if not start_date_str or not end_date_str:
            return CustomResponse.bad_request(
                message="Both start_date and end_date are required.",
                error={"start_date": start_date_str, "end_date": end_date_str},
            )

        try:
            start_date: datetime = self.parse_date(start_date_str)
            end_date: datetime = self.parse_date(end_date_str)
        except ValueError as e:
            return CustomResponse.bad_request(message=str(e))

        actual_days: int = v.get_actual_days(user, start_date, end_date)

        return CustomResponse.success(message="Balance calculated.", data=actual_days)


class AdminApplyVacationForUserApiView(GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AdminApplyVacationForUserSerializer

    def post(self, request: Request, user_id: str) -> Response:
        """
        ## Apply for Vacation on Behalf of Another User
        This function allows the administrator to apply for a vacation on behalf of another user, but only if they work in the same office.
        ### Parameters:
        - **user_id** (`int`): The ID of the user for whom the vacation is being requested.
        - **reason** (`str`): A string describing the reason for the vacation request.
        - **from_date** (`datetime`): The starting date of the vacation.
        - **end_date** (`datetime`): The ending date of the vacation.
        """
        admin = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            applying_user = get_user_by_id(user_id)
            if applying_user is None:
                return CustomResponse.not_found(message="User not found.")

            if applying_user.location.id != admin.location.id:
                return CustomResponse.unauthorized(
                    message=f"This action can only be performed by administrators who work in the {applying_user.location.name} office."
                )

            known_reasons = [
                REASON_CHOICES.ANNUAL_LEAVES,
                REASON_CHOICES.EMERGENCY_LEAVE,
                REASON_CHOICES.COMPENSATION,
                REASON_CHOICES.LEAVE_EXCUSES,
                REASON_CHOICES.UNPAID,
                REASON_CHOICES.SICK_LEAVES,
            ]
            reason = serializer.validated_data.get("reason")
            if reason not in known_reasons:
                formatted_string = (
                    ", ".join(known_reasons[:-1]) + f" and {known_reasons[-1]}"
                )
                return CustomResponse.bad_request(
                    message=f"reason {reason} is not valid, the available resons are {formatted_string}"
                )

            from_date = serializer.validated_data.get("from_date")
            end_date = serializer.validated_data.get("end_date")

            # Check if there are pending vacations in the same day
            pending_requests = Vacation.objects.filter(
                applying_user=applying_user,
                from_date__day=from_date.day,
                end_date__day=end_date.day,
                status=STATUS_CHOICES.PENDING,
            )

            if len(pending_requests) > 0:
                return CustomResponse.bad_request(
                    message="The selected user has another request with the same dates and pending status. Please review their previous request before submitting a new one."
                )

            # Check balance.
            v = StanderdVacationBalance()
            v.check(applying_user)

            user_reason_balance = applying_user.vacationbalance
            vacation_days = v.get_actual_days(applying_user, from_date, end_date)

            if reason == REASON_CHOICES.PUBLIC_HOLIDAYS:
                return CustomResponse.bad_request(
                    message=f"You have sent an invalid reason {reason}",
                    error={
                        "message": "This field should be one of the follwing reasons",
                        "reasons": [
                            reason
                            for reason in REASON_CHOICES
                            if reason != REASON_CHOICES.PUBLIC_HOLIDAYS
                        ],
                    },
                )

            curr_balance = getattr(user_reason_balance, reason)

            pending_vacations = Vacation.objects.filter(
                status=STATUS_CHOICES.PENDING,
                applying_user=applying_user,
                reason=reason,
            ).values_list("actual_days", flat=True)

            chcked_balance = curr_balance - sum(pending_vacations)

            if curr_balance < vacation_days:
                return CustomResponse.bad_request(
                    message=f"The user have only {curr_balance} days left of reason '{reason.capitalize().replace('_', ' ')}'"
                )

            if chcked_balance < vacation_days:
                return CustomResponse.bad_request(
                    message=f"The user have an additional pending request that deducts {sum(pending_vacations)} days from your balance even though the current balance for the '{reason.capitalize().replace('_', ' ')}' category is only {curr_balance} days."
                )

            saved_vacation = Vacation.objects.create(
                applying_user=applying_user,
                type=TYPE_CHOICES.VACATIONS,
                status=STATUS_CHOICES.PENDING,
                reason=reason,
                from_date=from_date,
                end_date=end_date,
                actual_days=vacation_days,
            )

            message = f"You have successfully applied for a {reason.capitalize().replace('_', ' ')} vacation for {applying_user.full_name}."
            if (
                reason == REASON_CHOICES.ANNUAL_LEAVES
                or reason == REASON_CHOICES.EMERGENCY_LEAVE
            ):
                message = f"You have successfully applied for an {reason.capitalize().replace('_', ' ')} vacation for {applying_user.full_name}."

            try:
                ping_redis()
            except:
                return http_ensure_redis_error()

            # Update the balance
            balance = v.check_and_update_balance(
                applying_user=saved_vacation.applying_user,
                vacation=saved_vacation,
                reason=saved_vacation.reason,
                start_date=saved_vacation.from_date,
                end_date=saved_vacation.end_date,
            )

            if balance is not True:
                return CustomResponse.bad_request(message=balance)

            # Approve the vacation.
            saved_vacation.status = STATUS_CHOICES.APPROVED
            saved_vacation.approval_user = admin
            saved_vacation.save()

            # set_notification_request_redis(serializer.data)
            response_data: Dict = wrap_vacation_request(saved_vacation)
            return CustomResponse.success(message=message, data=response_data)
        return CustomResponse.bad_request(
            message="Please make sure that you entered a valid data.",
            error=serializer.errors,
        )
