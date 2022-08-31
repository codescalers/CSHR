from rest_framework.serializers import ModelSerializer, SerializerMethodField

from server.cshr.models.users import User

from ..models.company_properties import Company_properties


class CompanyPropertiesSerializer(ModelSerializer):
    """
    This class will be used to get all info about company properties
    """

    user_obj = SerializerMethodField(read_only=True)

    class Meta:
        model = Company_properties
        fields =["name", "image_of", "user_obj"]

    def get_user_obj(self, obj: Company_properties) -> User:
        from server.cshr.serializers.users import GeneralUserSerializer
        return GeneralUserSerializer(obj.user).data
