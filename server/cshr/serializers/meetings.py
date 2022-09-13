from server.cshr.models.meetings import Meetings
from typing import Dict, List
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.users import User
from server.cshr.serializers.users import BaseUserSerializer


class MeetingsSerializer(ModelSerializer):
    """Class to serialize Meeting objects"""

    invited_users: List[User] = SerializerMethodField()
    date = SerializerMethodField()
    host_user = SerializerMethodField()

    class Meta:
        model = Meetings
        fields = ("id", "invited_users", "date", "meeting_link", "host_user","location")

    def get_invited_users(self, obj: Meetings) -> List[BaseUserSerializer]:
        """Returns a list of users that invited to the meeting."""
        return BaseUserSerializer(obj.invited_users.all(), many=True).data

    def get_host_user(self, obj: Meetings) -> BaseUserSerializer:
        """Returns the  host user that made the meeting."""
        return BaseUserSerializer(obj.host_user).data

    def get_date(self, obj: Meetings) -> Dict:
        return {
            "year": obj.date.year,
            "month": obj.date.month,
            "day": obj.date.day,
            "hour": obj.date.hour,
            "minute": obj.date.minute,
        }
