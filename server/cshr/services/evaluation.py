"""methods that will serve evaluation endpoints"""
from server.cshr.models.evaluations import Evaluations,UserEvaluations


def get_evaluation_by_id(id: str) -> UserEvaluations:
    try:
        return UserEvaluations.objects.get(id=int(id))
    except UserEvaluations.DoesNotExist:
        return None


def all_evaluations():
    try:
        return UserEvaluations.objects.all()
    except UserEvaluations.DoesNotExist:
        return None
