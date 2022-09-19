"""This file will containes everything related to User model."""
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from typing import Any, List, Union
from itertools import chain

from server.cshr.models.users import User, UserSkills


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


def filter_users_by_berithday_month(month: str) -> User:
    """Filter users based on birthdayes."""
    users: List[User] = User.objects.filter(birthday__month=month)
    return users


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


def get_user_team_leader_and_members(user: User) -> List[User]:
    """Return a list of members and team leaders"""
    team_leaders: List[User] = get_user_by_id(user.id).reporting_to.all().order_by('-created_at')
    members: List[User] = User.objects.filter(team=user.team).order_by('-created_at')
    objects: Union[List[Any], None] = list(chain(team_leaders, members))
    return objects
