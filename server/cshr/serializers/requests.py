from rest_framework import serializers

from server.cshr.models.requests import Requests


class RequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Requests
        fields = "__all__"