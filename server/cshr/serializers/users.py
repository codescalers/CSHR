from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.users import User


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

    def get_user_requests(self, obj):
        requests = obj.requests.all()
        return requests
