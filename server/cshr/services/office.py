"""
methods that will serve office endpoints
"""
from server.cshr.models.office import Office


def get_office_by_id(id: str) -> Office:
    try:
        return Office.objects.get(id=int(id))
    except Office.DoesNotExist:
        return None


def get_office_by_name(name: str) -> Office:
    try:
        return Office.objects.get(name=name)
    except Office.DoesNotExist:
        return None
