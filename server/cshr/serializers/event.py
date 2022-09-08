from typing import Dict
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.event import Event
from server.cshr.serializers.users import BaseUserSerializer


class EventSerializer(ModelSerializer):
    peoples = SerializerMethodField()
    date = SerializerMethodField()

    class Meta:
        model = Event
        fields = ["people", "name", "description", "location", "date", "peoples"]

    def get_peoples(self, obj: Event) -> BaseUserSerializer:
        return BaseUserSerializer(obj.people.all(), many=True).data

    def get_date(self, obj: Event) -> Dict:
        return {
            "year": obj.date.year,
            "month": obj.date.month,
            "day": obj.date.day,
            "hour": obj.date.hour,
            "minute": obj.date.minute,
        }
