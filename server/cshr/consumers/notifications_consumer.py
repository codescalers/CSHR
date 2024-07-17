import enum
import json
from typing import Dict, List, Optional

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from cshr.models.users import User
from cshr.services.users import build_user_reporting_to_hierarchy
from cshr.models.vacations import Vacation
from cshr.services.vacations import get_vacation_by_id
from cshr.models.requests import STATUS_CHOICES
from cshr.models.notification import Notification
from cshr.serializers.notification import NotificationSerializer


class RequestEvents(enum.Enum):
    """Enumeration for different types of request events."""

    POST_NEW_VACATION_REQUEST = "post_new_vacation_request"
    APPROVE_REQUEST = "approve_request"
    REJECT_REQUEST = "reject_request"
    REQUEST_TO_CANCEL_REQUEST = "request_to_cancel_request"
    APPROVE_CANCEL_REQUEST = "approve_cancel_request"
    REJECT_CANCEL_REQUEST = "reject_cancel_request"


class WSErrorWrapper:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

    def to_json(self) -> Dict[str, str]:
        return {"code": self.code, "message": self.message}


@database_sync_to_async
def _get_vacation_applying_user(vacation: Vacation) -> User:
    return vacation.applying_user


@database_sync_to_async
def _get_vacation_by_id(vacation_id: int) -> Vacation:
    return get_vacation_by_id(vacation_id)


@database_sync_to_async
def _build_user_reporting_to_hierarchy(applying_user: User) -> List[int]:
    return build_user_reporting_to_hierarchy(applying_user)


@database_sync_to_async
def _get_request_notification_for_receiver_based_on_status(
    request_id: int, receiver_id: int, status: STATUS_CHOICES
) -> Optional[Notification]:
    try:
        return Notification.objects.get(
            request__id=request_id,
            receiver__id=receiver_id,
            request_status=status,
        )
    except Notification.DoesNotExist:
        return None


@database_sync_to_async
def get_notification_serializer(notification: Notification) -> Dict:
    return NotificationSerializer(notification).data


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = f"room_{self.room_name}"
        self.error = WSErrorWrapper(code=0, message="")

        if self.scope.get("user") and self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            print(f"User {self.user} connected to {self.group_name}")
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            self.error.message = (
                "Cannot connect to the Websocket due to: User is Anonymous."
            )
            self.error.code = 401
            await self.disconnect(close_code=self.error.code)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"Disconnection code: {close_code}")
        if self.error.code != 0:
            error_message = self.error.to_json()
            await self.accept()
            await self.send(text_data=json.dumps(error_message))
        await self.close()

    async def receive(self, text_data, bytes_data=None):
        data: Dict = json.loads(text_data)
        request_event = data.get("event")

        if not request_event:
            await self.handle_error(400, "The request must contain an event type.")
            return

        event_handler = {
            RequestEvents.POST_NEW_VACATION_REQUEST.value: self.post_new_vacation_request,
            RequestEvents.REQUEST_TO_CANCEL_REQUEST.value: self.request_to_cancel_request,
            RequestEvents.APPROVE_CANCEL_REQUEST.value: self.approve_cancel_request,
            RequestEvents.REJECT_CANCEL_REQUEST.value: self.reject_cancel_request,
            RequestEvents.APPROVE_REQUEST.value: self.approve_request,
            RequestEvents.REJECT_REQUEST.value: self.reject_request,
        }.get(request_event)

        if event_handler:
            await event_handler(data)

    async def handle_error(self, code: int, message: str):
        self.error.code = code
        self.error.message = message
        await self.send_to_group_name(self.error.to_json())

    async def send_message(self, data: Dict):
        await self.send(text_data=json.dumps(data))

    async def send_to_group_name(self, data: Dict, group_name: Optional[str] = None):
        if not group_name:
            group_name = self.group_name
        data["type"] = "send_message"
        await self.channel_layer.group_send(group_name, data)

    async def post_new_vacation_request(self, data: Dict):
        await self.handle_vacation_request(
            data, RequestEvents.POST_NEW_VACATION_REQUEST, STATUS_CHOICES.PENDING
        )

    async def request_to_cancel_request(self, data: Dict):
        await self.handle_vacation_request(
            data,
            RequestEvents.REQUEST_TO_CANCEL_REQUEST,
            STATUS_CHOICES.REQUESTED_TO_CANCEL,
        )

    async def approve_request(self, data: Dict):
        await self.handle_single_receiver_request(
            data, RequestEvents.APPROVE_REQUEST, STATUS_CHOICES.APPROVED
        )

    async def reject_request(self, data: Dict):
        await self.handle_single_receiver_request(
            data, RequestEvents.REJECT_REQUEST, STATUS_CHOICES.REJECTED
        )

    async def approve_cancel_request(self, data: Dict):
        await self.handle_single_receiver_request(
            data, RequestEvents.APPROVE_CANCEL_REQUEST, STATUS_CHOICES.CANCEL_APPROVED
        )

    async def reject_cancel_request(self, data: Dict):
        await self.handle_single_receiver_request(
            data, RequestEvents.REJECT_CANCEL_REQUEST, STATUS_CHOICES.CANCEL_REJECTED
        )

    async def handle_vacation_request(
        self, data: Dict, event: RequestEvents, status: STATUS_CHOICES
    ):
        request_id = data.get("request_id")
        if not request_id:
            await self.handle_error(
                400,
                f"The request event type is '{event.value}', but no vacation ID has been submitted.",
            )
            return

        vacation: Vacation = await _get_vacation_by_id(request_id)
        applying_user: User = await _get_vacation_applying_user(vacation)
        receivers_ids: List[int] = await _build_user_reporting_to_hierarchy(
            applying_user
        )

        for receiver_id in receivers_ids:
            group_name = f"room_{receiver_id}"
            notification = await _get_request_notification_for_receiver_based_on_status(
                request_id, receiver_id, status
            )
            if notification:
                notification_serializer = await get_notification_serializer(
                    notification
                )
                notification_serializer["request"]["from_date"] = (
                    notification_serializer["request"]["from_date"].isoformat()
                )
                notification_serializer["request"]["end_date"] = (
                    notification_serializer["request"]["end_date"].isoformat()
                )
                await self.send_to_group_name(notification_serializer, group_name)

    async def handle_single_receiver_request(
        self, data: Dict, event: RequestEvents, status: STATUS_CHOICES
    ):
        request_id = data.get("request_id")
        if not request_id:
            await self.handle_error(
                400,
                f"The request event type is '{event.value}', but no request ID has been submitted.",
            )
            return

        vacation: Vacation = await _get_vacation_by_id(request_id)
        applying_user: User = await _get_vacation_applying_user(vacation)
        self.group_name = f"room_{applying_user.id}"
        notification = await _get_request_notification_for_receiver_based_on_status(
            request_id, applying_user.id, status
        )
        if notification:
            notification_serializer = await get_notification_serializer(notification)
            notification_serializer["request"]["from_date"] = notification_serializer[
                "request"
            ]["from_date"].isoformat()
            notification_serializer["request"]["end_date"] = notification_serializer[
                "request"
            ]["end_date"].isoformat()
            await self.send_to_group_name(notification_serializer)
