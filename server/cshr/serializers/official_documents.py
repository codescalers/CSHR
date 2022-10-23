from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from server.cshr.models.official_documents import OffcialDocument
from server.cshr.serializers.users import TeamSerializer


class OffcialDocumentSerializer(ModelSerializer):
    """Class OffcialDocumentSerializer to serialize document object."""

    applying_user = SerializerMethodField()
    status = SerializerMethodField()
    type = SerializerMethodField()
    created_at = SerializerMethodField()

    class Meta:
        model = OffcialDocument
        fields = ["document", "applying_user", "status", "type", "created_at", "id"]

    def get_applying_user(self, obj: OffcialDocument) -> TeamSerializer:
        """
        this function return request's applying user
        """
        return TeamSerializer(obj.applying_user).data

    def get_status(self, obj: OffcialDocument) -> str:
        """
        this function return request's status
        """
        return obj.status

    def get_type(self, obj: OffcialDocument) -> str:
        """
        this function return request's type
        """
        return obj.type

    def get_created_at(self, obj: OffcialDocument) -> str:
        """
        this function return request's created_at
        """
        return obj.created_at
