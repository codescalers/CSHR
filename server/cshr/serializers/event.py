from rest_framework.serializers import ModelSerializer
from cshr.models.event import Event


class EventSerializer(ModelSerializer):
    # custom_people = SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            # "people",
            # "custom_people",
            "name",
            "description",
            # "location",
            "from_date",
            "end_date",
        ]

    # def get_custom_people(self, obj: Event) -> BaseUserSerializer:
    #     return BaseUserSerializer(obj.people.all(), many=True).data


class EventOnDaySerializer(ModelSerializer):
    # custom_people = SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            # "people",
            # "custom_people",
            "name",
            "description",
            # "location",
            "from_date",
            "end_date",
        ]

    # def get_custom_people(self, obj: Event) -> BaseUserSerializer:
    #     return BaseUserSerializer(obj.people.all(), many=True).data
