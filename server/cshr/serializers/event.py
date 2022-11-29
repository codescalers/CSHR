from typing import Dict
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.event import Event
from server.cshr.serializers.users import BaseUserSerializer


class EventSerializer(ModelSerializer):
    custom_people = SerializerMethodField()
    from_date = SerializerMethodField()
    end_date = SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "people",
            "custom_people",
            "name",
            "description",
            "location",
            "from_date",
            "end_date",
        ]

    def get_custom_people(self, obj: Event) -> BaseUserSerializer:
        return BaseUserSerializer(obj.people.all(), many=True).data

    def get_from_date(self, obj: Event) -> Dict:
        return {
            "year": obj.from_date.year,
            "month": obj.from_date.month,
            "day": obj.from_date.day,
            "hour": obj.from_date.hour,
            "minute": obj.from_date.minute,
        }

    def get_end_date(self, obj: Event) -> Dict:
        return {
            "year": obj.end_date.year,
            "month": obj.end_date.month,
            "day": obj.end_date.day,
            "hour": obj.end_date.hour,
            "minute": obj.end_date.minute,
        }


class EventOnDaySerializer(ModelSerializer):
    custom_people = SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "people",
            "custom_people",
            "name",
            "description",
            "location",
            "from_date",
            "end_date",
        ]

    def get_custom_people(self, obj: Event) -> BaseUserSerializer:
        return BaseUserSerializer(obj.people.all(), many=True).data
