from server.cshr.models.users import User, UserSkills
from django.contrib.auth.hashers import check_password

from django.db.models import Q


def get_user_by_id(id: str) -> User:
    """Return user who have the same id"""
    try:
        return User.objects.get(id=int(id))
    except User.DoesNotExist:
        return None


def get_user_by_email(email: str) -> User:
    """Return user who have the same email"""
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def get_user_by_full_name(first_name: str, last_name: str) -> User:
    """Return user who have the same email"""
    try:
        return User.objects.get(first_name=first_name, last_name=last_name)
    except User.DoesNotExist:
        return None


def success_login_user(email, password) -> User:
    """Return user who have the same email and password"""

    user = get_user_by_email(email=email)
    if user is not None:
        if check_password(password, user.password):
            return user
        return None
    return None


def get_user_type_by_id(id: str) -> User:
    """Return user type by id"""
    try:
        user = User.objects.get(id=int(id))
        return user.user_type
    except User.DoesNotExist:
        return None


def get_users_filter(
    search_input: str,
) -> User:
    """Return users by filters"""

    users = User.objects.filter(
        Q(email__icontains=search_input)
        | Q(first_name__icontains=search_input)
        | Q(last_name__icontains=search_input)
    )
    return users


def get_all_of_users() -> User:
    """Return all users"""
    return User.objects.all()


def get_or_create_skill_by_name(name: str) -> UserSkills or bool:
    """Return a skill by name"""
    return UserSkills.objects.get_or_create(name=name.lower())
