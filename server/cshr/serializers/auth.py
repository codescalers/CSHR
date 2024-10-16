from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.settings import api_settings
from cshr.serializers.Image_upload import Base64ImageField
from rest_framework import exceptions
from django.contrib.auth.hashers import check_password
from typing import Dict, Any
from cshr.models.users import User
from cshr.services.users import get_user_by_email, get_user_by_id


class ChangePasswordSerializer(Serializer):
    old_password = CharField()
    new_password = CharField()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Override TokenObtainPairSerializer to add extra responses"""

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        if hasattr(user, "permission"):
            token["permission"] = user.permission
        return token

    def validate(self, attrs: Any) -> Dict[str, Any]:
        data = {}
        attrs["email"] = attrs.get("email")

        self.user = get_user_by_email(attrs["email"])
        if self.user is None:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        if check_password(attrs.get("password"), self.user.password):
            if api_settings.USER_AUTHENTICATION_RULE(self.user):
                self.user.md5_from_old_system = None
                self.user.save()
                return self.custom_token(data)
            try:
                user = User.objects.get(email=attrs["email"])
                self.user = user
                return self.custom_token(data)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    self.error_messages["no_active_account"],
                    "no_active_account",
                )
        raise exceptions.AuthenticationFailed(
            self.error_messages["no_active_account"],
            "no_active_account",
        )

    def custom_token(self, data: Dict):
        refresh = self.get_token(self.user)
        data["refresh_token"] = str(refresh)
        data["access_token"] = str(refresh.access_token)
        data["email"] = self.user.email
        data["full_name"] = self.user.full_name
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["id"] = self.user.id
        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    """serializer to refresh user token"""

    def validate(self, attrs: Any) -> Dict[str, Any]:
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data["access"], verify=True)
        user_id = decoded_payload["user_id"]
        user = get_user_by_id(user_id)
        refresh = RefreshToken.for_user(user)
        data["refresh"] = str(refresh)
        return data


class RegisterSerializer(ModelSerializer):
    """class RegisterSerializer to serialize the user obj"""

    image = Base64ImageField(
        max_length=None,
        use_url=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "telegram_link",
            "email",
            "birthday",
            "joining_at",
            "mobile_number",
            "password",
            "location",
            "team",
            "salary",
            "user_type",
            "reporting_to",
            "image",
            "gender",
            "job_title",
            "address",
            "social_insurance_number",
        )

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        reporting_to = validated_data.pop("reporting_to", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        for user in reporting_to:
            instance.reporting_to.add(user)
        return instance
