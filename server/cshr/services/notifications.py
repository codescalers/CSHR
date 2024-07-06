from typing import List, Union
from cshr.models.notification import Notification
from cshr.models.users import User
from cshr.models.requests import Requests


class VacationRequestNotification:
    """
    Handles creation of vacation request notifications.

    Attributes:
        sender (User): The user sending the notification.
        body (str): The body content of the notification.
        title (str): The title of the notification.
    """
    def __init__(self, sender: User):
        self.sender = sender
        self.body = None
        self.title = None

    def post_new_vacation(self, vacation_type: str, request: Requests) -> Notification:
        """
        Creates a new vacation request notification.

        Args:
            vacation_type (str): The type of vacation being requested.
            request (Requests): The request object associated with the vacation.

        Returns:
            Notification: The created notification object.
        """
        vacation_type = vacation_type.replace("_", " ").title()
        self.title = f"A new vacation request has been submitted by {self.sender.full_name}."
        self.body = f"{self.sender.full_name} requested a new {vacation_type} vacation."
        return Notification(
            title=self.title,
            body=self.body,
            request=request
        )

    def approve_vacation(self, vacation_type: str, request: Requests) -> Notification:
        """
        Creates a new vacation request notification.

        Args:
            vacation_type (str): The type of vacation being requested.
            request (Requests): The request object associated with the vacation.

        Returns:
            Notification: The created notification object.
        """

        vacation_type = vacation_type.replace("_", " ").title()
        self.title = f"Your {vacation_type} request has been approved by {self.sender.full_name}."
        self.body = f"{self.sender.full_name} approved your {vacation_type} request."

        return Notification(
            title=self.title,
            body=self.body,
            request=request
        )

    def reject_vacation(self, vacation_type: str, request: Requests) -> Notification:
        """
        Creates a new vacation request notification.

        Args:
            vacation_type (str): The type of vacation being requested.
            request (Requests): The request object associated with the vacation.

        Returns:
            Notification: The created notification object.
        """

        vacation_type = vacation_type.replace("_", " ").title()
        self.title = f"Your {vacation_type} request has been rejected by {self.sender.full_name}."
        self.body = f"{self.sender.full_name} rejected your {vacation_type} request."

        return Notification(
            title=self.title,
            body=self.body,
            request=request
        )


class NotificationsService:
    """
    Manages sending and retrieving notifications.

    Attributes:
        sender (User): The user sending the notifications.
        receivers (List[User]): The users receiving the notifications.
        vacations (VacationRequestNotification): An instance of the vacation request notification handler.
    """
    def __init__(self, sender: User, receivers: List[User]):
        self.sender = sender
        self.receivers = receivers
        self.vacations = VacationRequestNotification(self.sender)

    def push(self, notification: Notification) -> Notification:
        """
        Pushes a notification to the specified receivers.

        Args:
            notification (Notification): The notification object to be sent.

        Returns:
            Notification: The saved notification object.
        """
        notification = Notification.objects.create(
            title=notification.title,
            body=notification.body,
            sender=self.sender,
            request=notification.request,
        )
        notification.receivers.set(self.receivers)
        notification.save()
        return notification

    def create(self) -> Notification:
        """
        Creates a new notification without pushing it.

        Returns:
            Notification: The created notification object.
        """
        return Notification.objects.create(
            sender=self.sender,
            receivers=self.receivers,
            title=self.title,
            body=self.body,
        )

    def get_all(self) -> List[Notification]:
        """
        Retrieves all notifications.

        Returns:
            List[Notification]: A list of all notifications.
        """
        return Notification.objects.all()

    def get_for_sender(self) -> List[Notification]:
        """
        Retrieves notifications sent by the sender.

        Returns:
            List[Notification]: A list of notifications sent by the sender.
        """
        return Notification.objects.filter(sender=self.sender)

    @staticmethod
    def filter_based_on_receiver(receiver: User) -> List[Notification]:
        """
        Retrieves notifications received by a specific user.

        Args:
            receiver (User): The user receiving the notifications.

        Returns:
            List[Notification]: A list of notifications received by the user.
        """
        return Notification.objects.filter(receivers__in=[receiver]).order_by("-created_at")

    def filter_based_on_receivers(self) -> List[Notification]:
        """
        Retrieves notifications for the specified receivers.

        Returns:
            List[Notification]: A list of notifications for the receivers.
        """
        return Notification.objects.filter(receivers__in=self.receivers)

    @staticmethod
    def get_by_id(notification_id: Union[str, int]) -> Union[Notification, None]:
        """
        Retrieves a notification by its ID.

        Args:
            notification_id (Union[str, int]): The ID of the notification.

        Returns:
            Union[Notification, None]: The notification object if found, otherwise None.
        """
        if str(notification_id).isdigit():
            try:
                return Notification.objects.get(id=int(notification_id))
            except Notification.DoesNotExist:
                return None
        return None
