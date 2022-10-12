from rest_framework import serializers


class NotificationsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255)
    user = serializers.CharField(max_length=100)

    class Meta:
        fields = ('title', 'url','user',)