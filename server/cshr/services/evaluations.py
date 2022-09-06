"""methods that will serve evaluation endpoints"""
from server.cshr.models.evaluations import UserEvaluations


def get_evaluation_by_id(id: str) -> UserEvaluations:
    try:
        return UserEvaluations.objects.get(id=int(id))
    except UserEvaluations.DoesNotExist:
        return None


def all_evaluations():
    return UserEvaluations.objects.all()


def get_evaluations_for_a_user(id: int) -> UserEvaluations:
    return UserEvaluations.objects.filter(user=id)
