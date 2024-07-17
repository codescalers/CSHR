import enum
import json
from typing import Dict, List

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from cshr.models.users import User
from cshr.services.users import build_user_reporting_to_hierarchy, get_user_by_id
from cshr.services.notifications import NotificationsService
from cshr.models.vacations import Vacation
from cshr.services.vacations import get_vacation_by_id
from cshr.models.requests import Requests
from cshr.models.notification import Notification
from cshr.serializers.notification import NotificationSerializer


class RequestEvents(enum.Enum):
    """Enumeration for different types of request events."""

    POST_NEW_VACATION_REQUEST = "post_new_vacation_request"
    APPROVE_REQUEST = "approve_request"
    REJECT_REQUEST = "reject_request"


class WSErrorWrapper:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

    def to_json(self) -> Dict:
        return {"code": self.code, "message": self.message}


@database_sync_to_async
def _get_vacation_applying_user(vacation: Vacation) -> User:
    """Fetch the user who applied for the vacation."""
    return vacation.applying_user


@database_sync_to_async
def _get_vacation_by_id(vacation_id: int) -> Vacation:
    """Retrieve a vacation instance by its ID."""
    return get_vacation_by_id(vacation_id)


@database_sync_to_async
def _build_user_reporting_to_hierarchy(applying_user: User) -> List[int]:
    """Build a hierarchical list of user IDs to whom the user reports."""
    return build_user_reporting_to_hierarchy(applying_user)


@database_sync_to_async
def _push_notification_to_receiver(
    applying_user: User, receiver_id: int, vacation: Vacation
) -> Notification:
    """Push a notification to the specified receiver."""
    receiver = get_user_by_id(receiver_id)
    notification = NotificationsService(sender=applying_user, receiver=receiver)
    request = Requests.objects.get(id=vacation.id)
    message = notification.vacations.post_new_vacation(vacation.reason, request)
    notification = notification.push(message)
    return notification


@database_sync_to_async
def _push_approve_notification_to_applying_user(vacation: Vacation) -> Notification:
    """Push a notification to the specified receivers."""
    notification = NotificationsService(
        sender=vacation.approval_user, receiver=vacation.applying_user
    )
    request = Requests.objects.get(id=vacation.id)
    message = notification.vacations.approve_vacation(vacation.reason, request)
    notification = notification.push(message)
    return notification


@database_sync_to_async
def _push_reject_notification_to_applying_user(vacation: Vacation) -> Notification:
    """Push a notification to the specified receivers."""
    notification = NotificationsService(
        sender=vacation.approval_user, receiver=vacation.applying_user
    )
    request = Requests.objects.get(id=vacation.id)
    message = notification.vacations.reject_vacation(vacation.reason, request)
    notification = notification.push(message)
    return notification


@database_sync_to_async
def _get_request_notification_for_receiver(
    request_id: int, receiver_id: int
) -> Notification:
    """Get the Notification based on the request id and the receiver id."""
    try:
        return Notification.objects.get(
            request__id=int(request_id), receiver__id=int(receiver_id)
        )
    except Notification.DoesNotExist:
        return None


@database_sync_to_async
def get_notification_serializer(notification: Notification) -> Dict:
    """Serialize the notification instance."""
    return NotificationSerializer(notification).data


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handle a new WebSocket connection.

        If the user is authenticated, they are added to a group based on the room ID.
        """
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
        """
        Handle WebSocket disconnection.

        The user is removed from their group and the connection is closed.
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"Disconnection code: {close_code}")
        if self.error.code != 0:
            error_message = self.error.to_json()
            await self.accept()
            await self.send(text_data=json.dumps(error_message))
        # TODO: Handle the close code.
        await self.close()

    async def receive(self, text_data, bytes_data=None):
        """
        Handle receiving data from the WebSocket.

        The data is processed and a notification is pushed to the relevant users.
        """
        data: Dict = json.loads(text_data)

        request_event = data.get("event")
        if not request_event:
            self.error.code = 400
            self.error.message = "The request must contain an event type."
            return await self.send_to_group_name(self.error.to_json())

        if request_event == RequestEvents.POST_NEW_VACATION_REQUEST.value:
            return await self.post_new_vacation_request(data)
        elif request_event == RequestEvents.APPROVE_REQUEST.value:
            return await self.approve_request(data)
        elif request_event == RequestEvents.REJECT_REQUEST.value:
            return await self.reject_request(data)

    async def send_message(self, data: Dict):
        """
        Send a message to the WebSocket.

        This function is called when a message needs to be sent to the WebSocket.
        """
        await self.send(text_data=json.dumps(data))

    async def send_to_group_name(self, data: Dict, group_name: str):
        """
        Send a message to a specific group.

        The message is sent to all members of the specified group.
        """
        data["type"] = "send_message"
        await self.channel_layer.group_send(group_name, data)

    async def post_new_vacation_request(self, data: Dict):
        """
        Handle the 'post_new_vacation' event by processing the provided data and sending notifications.

        Args:
            data (Dict): The data received from the WebSocket, expected to contain event and vacation information.

        Returns:
            None
        """
        vacation_data = data.get("vacation")

        if not vacation_data:
            self.error.code = 400
            self.error.message = f"The request event type is '{RequestEvents.POST_NEW_VACATION_REQUEST.value}', but no vacation has been submitted."
            return await self.send_to_group_name(self.error.to_json(), self.group_name)

        vacation_id = vacation_data.get("id")
        if not vacation_id:
            self.error.code = 400
            self.error.message = f"The request event type is '{RequestEvents.POST_NEW_VACATION_REQUEST.value}', but no vacation ID has been submitted."
            return await self.send_to_group_name(self.error.to_json(), self.group_name)

        vacation: Vacation = await _get_vacation_by_id(vacation_id)
        applying_user: User = await _get_vacation_applying_user(vacation)
        receivers_ids: List[int] = await _build_user_reporting_to_hierarchy(
            applying_user
        )

        for receiver_id in receivers_ids:
            self.group_name = f"room_{receiver_id}"
            notification = await _get_request_notification_for_receiver(
                vacation_id, receiver_id
            )
            if notification is not None:
                notification_serializer = await get_notification_serializer(
                    notification
                )
                notification_serializer["request"]["from_date"] = (
                    notification_serializer["request"]["from_date"].isoformat()
                )
                notification_serializer["request"]["end_date"] = (
                    notification_serializer["request"]["end_date"].isoformat()
                )
                await self.send_to_group_name(notification_serializer, self.group_name)

    async def approve_request(self, data: Dict):
        request_id = data.get("request_id")

        if not request_id:
            self.error.code = 400
            self.error.message = f"The request event type is '{RequestEvents.APPROVE_VACATION.value}', but no request ID has been submitted."
            return await self.send_to_group_name(self.error.to_json(), self.group_name)

        vacation = await _get_vacation_by_id(request_id)
        applying_user = await _get_vacation_applying_user(vacation)
        self.group_name = f"room_{applying_user.id}"
        notification = await _get_request_notification_for_receiver(
            request_id, applying_user.id
        )

        if notification is not None:
            notification_serializer = await get_notification_serializer(notification)
            notification_serializer["request"]["from_date"] = notification_serializer[
                "request"
            ]["from_date"].isoformat()
            notification_serializer["request"]["end_date"] = notification_serializer[
                "request"
            ]["end_date"].isoformat()
            await self.send_to_group_name(notification_serializer, self.group_name)

    async def reject_request(self, data: Dict):
        request_id = data.get("request_id")

        if not request_id:
            self.error.code = 400
            self.error.message = f"The request event type is '{RequestEvents.APPROVE_VACATION.value}', but no request ID has been submitted."
            return await self.send_to_group_name(self.error.to_json(), self.group_name)

        vacation = await _get_vacation_by_id(request_id)
        applying_user = await _get_vacation_applying_user(vacation)
        self.group_name = f"room_{applying_user.id}"
        notification = await _get_request_notification_for_receiver(
            request_id, applying_user.id
        )

        if notification is not None:
            notification_serializer = await get_notification_serializer(notification)
            notification_serializer["request"]["from_date"] = notification_serializer[
                "request"
            ]["from_date"].isoformat()
            notification_serializer["request"]["end_date"] = notification_serializer[
                "request"
            ]["end_date"].isoformat()
            await self.send_to_group_name(notification_serializer, self.group_name)
