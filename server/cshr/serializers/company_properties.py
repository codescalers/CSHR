from rest_framework.serializers import ModelSerializer, SerializerMethodField
 
 
from ..models.company_properties import Company_properties
 
 



class CompanyPropertiesSerializer(ModelSerializer):
    """
    This class will be used to get all info about a training course
    """
    user = SerializerMethodField(read_only= True)
    class Meta:
        model = Company_properties
        fields = "__all__"