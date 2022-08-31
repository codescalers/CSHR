from rest_framework.serializers import ModelSerializer, SerializerMethodField


from ..models.company_properties import CompanyProperties


class CompanyPropertiesSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """

    user = SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyProperties
        fields = "__all__"
