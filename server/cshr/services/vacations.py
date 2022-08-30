from server.cshr.models.vacations import Vacation


def get_vacation_by_id(id: str) -> Vacation:
    """Return vacation who have the same id"""
    try:
        return Vacation.objects.get(id=int(id))
    except Vacation.DoesNotExist:
        return None


def get_all_vacations() -> Vacation:
    """Return all hr letters"""
    return Vacation.objects.all()
