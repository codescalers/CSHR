from rest_framework.serializers import ModelSerializer
from server.cshr.models.meetings import Meetings


class MeetingsSerializer(ModelSerializer):
    class Meta:
        model = Meetings
        exclude = ("host_user",)
