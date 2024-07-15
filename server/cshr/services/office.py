"""
methods that will serve office endpoints
"""

from cshr.models.office import Office
from django.db.models.query import QuerySet

from cshr.models.users import User, USER_TYPE


def get_office_by_id(id: str) -> Office:
    if not str(id).isdigit():
        return None
    try:
        return Office.objects.get(id=int(id))
    except Office.DoesNotExist:
        return None


def get_office_by_name(name: str) -> Office:
    try:
        return Office.objects.get(name=name)
    except Office.DoesNotExist:
        return None


def get_office_supervisors(office: Office) -> QuerySet[User]:
    return User.objects.filter(location__id=office.id, user_type=USER_TYPE.SUPERVISOR)

def filter_office_admins_by_id(office: Office, flat_id: bool = False) -> QuerySet[User]:
    users = User.objects.filter(location__id=office.id, user_type=USER_TYPE.ADMIN)
    if flat_id:
        return users.values_list('id', flat=flat_id)
    return users