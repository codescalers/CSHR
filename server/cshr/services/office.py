"""
methods that will serve office endpoints
"""
from server.cshr.models.office import Office


def get_office_by_id(id: str) -> Office:
    try:
        return Office.objects.get(id=int(id))
    except Office.DoesNotExist:
        return None
