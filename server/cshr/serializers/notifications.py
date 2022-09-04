from xml.etree.ElementInclude import include
from rest_framework.serializers import ModelSerializer
from server.cshr.models.notifications import Notifications


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"
