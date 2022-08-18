from rest_framework import serializers
from server.cshr.models.office import Office

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields =["name","country"]