from server.cshr.models.compensation import Compensation
from server.cshr.models.requests import STATUS_CHOICES


def get_compensation_by_id(id: str) -> Compensation:
    """Return compensation who have the same id"""
    try:
        return Compensation.objects.get(id=int(id))
    except Compensation.DoesNotExist:
        return None


def get_all_compensations() -> Compensation:
    """Return all compensations"""
    return Compensation.objects.all()


def filter_all_compensations_by_pinding_status() -> Compensation:
    """Return all compensations"""
    return Compensation.objects.filter(status=STATUS_CHOICES.PENDING)


def get_compensations_by_user(user: str) -> Compensation:
    "Return all compensations for certain user"
    return Compensation.objects.filter(applying_user=user)
