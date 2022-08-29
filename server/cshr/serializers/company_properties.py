
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from server.cshr.models.company_properties import Company_properties


class CompanyPropertiesSerializer(ModelSerializer):
    """class CompanyPropertiesSerializer to serialize the user obj"""


    user = SerializerMethodField(read_only=True)

    class Meta:
        model = Company_properties
        fields = ["name", "image_of", "user"]

    def get_user(self, obj):
        return obj.user.id
