"""methods that will serve evaluation endpoints"""
from server.cshr.models.evaluations import UserEvaluations


def get_user_evaluation_by_id(id: str) -> UserEvaluations:
    try:
        return UserEvaluations.objects.get(id=int(id))
    except UserEvaluations.DoesNotExist:
        return None


def all_user_evaluations():

    return UserEvaluations.objects.all()
