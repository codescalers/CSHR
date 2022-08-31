from rest_framework.serializers import ModelSerializer
from server.cshr.models.event import Event


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
