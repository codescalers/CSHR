"""methods that will serve evaluation endpoints"""
from server.cshr.models.evaluations import Evaluations


def get_evaluation_by_id(id: str) -> Evaluations:
    try:
        return Evaluations.objects.get(id=int(id))
    except Evaluations.DoesNotExist:
        return None


def all_evaluations():
    try:
        return Evaluations.objects.all()
    except Evaluations.DoesNotExist:
        return None
