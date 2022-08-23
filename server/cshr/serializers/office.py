from rest_framework.serializers import ModelSerializer
from server.cshr.models.office import Office


class OfficeSerializer(ModelSerializer):
    """
    This class will be used to get all info about an office
    """

    class Meta:
        model = Office
        fields = ["id", "name", "country"]


class OfficeUpdateSerializer(ModelSerializer):
    class Meta:
        model = Office
        fields = ["name", "country"]  # and whatever other fields you want to expose
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "country": {"required": False, "allow_null": True},
        }
