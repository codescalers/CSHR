from cshr.models.meetings import Meetings
from typing import List
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from cshr.models.users import User
from cshr.serializers.users import BaseUserSerializer


class MeetingsSerializer(ModelSerializer):
    """Class to serialize Meeting objects"""

    invited_users: List[User] = SerializerMethodField()
    host_user: User = SerializerMethodField()

    class Meta:
        model = Meetings
        fields = (
            "id",
            "invited_users",
            "date",
            "meeting_link",
            "host_user",
            "location",
        )

    def get_invited_users(self, obj: Meetings) -> List[BaseUserSerializer]:
        """Returns a list of users that invited to the meeting."""
        return BaseUserSerializer(obj.invited_users.all(), many=True).data

    def get_host_user(self, obj: Meetings) -> BaseUserSerializer:
        """Returns the  host user that made the meeting."""
        return BaseUserSerializer(obj.host_user).data
