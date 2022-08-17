from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.users import User
import base64
from django.conf import settings
import os


class UserSerializer(ModelSerializer):
    """
    This class will be used to get all info about a user
    """
    user_location = SerializerMethodField()
    user_skills = SerializerMethodField()
    user_requests = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "image", "mobile_number", "telegram_link",
            "birthday", "team", "user_location", "user_skills"
        ]

    def get_user_location(self, obj):
        location = obj.location
        return location.name

    def get_user_skills(self, obj):
        skills = obj.skills
        return skills.all()

    def encode_profile_image(self, user):
        with open(os.path.join(settings.MEDIA_ROOT, user.image.name), "rb") as image_file:
            return base64.b64encode(image_file.read())
