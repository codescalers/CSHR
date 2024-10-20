from rest_framework.serializers import ModelSerializer, SerializerMethodField

from cshr.models.users import User

from cshr.models.company_properties import CompanyProperties


class CompanyPropertiesSerializer(ModelSerializer):
    """
    This class will be used to get all info about company properties
    """

    user_obj = SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyProperties
        fields = ["name", "image_of", "user_obj"]

    def get_user_obj(self, obj: CompanyProperties) -> User:
        from cshr.serializers.users import TeamSerializer

        return TeamSerializer(obj.user).data
