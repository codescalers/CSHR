from server.cshr.models.compensation import Compensation


def get_compensation_by_id(id: str) -> Compensation:
    """Return compensation who have the same id"""
    try:
        return Compensation.objects.get(id=int(id))
    except Compensation.DoesNotExist:
        return None


def get_all_compensations() -> Compensation:
    """Return all compensations"""
    return Compensation.objects.all()
