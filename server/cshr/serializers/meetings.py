from typing import List
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.meetings import Meetings
from server.cshr.models.users import User
from server.cshr.serializers.users import BaseUserSerializer


class MeetingsSerializer(ModelSerializer):
    """Class to serialize Meeting objects"""

    invited_users: List[User] = SerializerMethodField()

    class Meta:
        model = Meetings
        fields = ("invited_users", "date", "meeting_link")

    def get_invited_users(self, obj: Meetings) -> List[BaseUserSerializer]:
        """Returns a list of users that invited to the meeting."""
        return BaseUserSerializer(obj.invited_users.all(), many=True).data
