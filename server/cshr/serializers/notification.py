from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer, BooleanField

from cshr.models.notification import Notification
from cshr.models.requests import TYPE_CHOICES, Requests
from cshr.serializers.requests import RequestsSerializer
from cshr.services.vacations import get_vacation_by_id
from cshr.services.users import build_user_reporting_to_hierarchy

class NotificationSerializer(ModelSerializer):
  """
    Serializer for Notification model to serialize/deserialize Notification objects.
    Fields included: sender, receivers, title, body, is_read, request.

    Attributes:
        request (SerializerMethodField): Method field to serialize the related Request object.

    Inherits:
        ModelSerializer: Provides serialization and deserialization capabilities for the Notification model.

    Methods:
        get_request: Custom method to serialize the related Request object for the notification.
  """
  request = SerializerMethodField()

  class Meta:
    model = Notification
    fields = "__all__"

  def get_request(self, obj: Notification):
    """
      Custom method to serialize the related Request object for the notification.

      Parameters:
          obj (Notification): The Notification object for which the related Request object needs to be serialized.

      Returns:
          dict: A serialized representation of the related Request object.

    """
    request: Requests = obj.request
    request_serializer = RequestsSerializer(request).data
    if obj.request.type == TYPE_CHOICES.VACATIONS:
      vacation = get_vacation_by_id(obj.request.id)
      if vacation:
        request_serializer["from_date"] = vacation.from_date
        request_serializer["end_date"] = vacation.end_date
        request_serializer["approvals"] = build_user_reporting_to_hierarchy(vacation.applying_user)
    return request_serializer


class ReadNotificationSerializer(Serializer):
  is_read = BooleanField()