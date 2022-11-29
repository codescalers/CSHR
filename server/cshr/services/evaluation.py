"""methods that will serve evaluation endpoints"""
from server.cshr.models.evaluations import UserEvaluations, Evaluations
from server.cshr.models.users import User


def get_evaluation_by_id(id: str) -> Evaluations:
    """get evaluation by id"""
    try:
        return Evaluations.objects.get(id=int(id))
    except Evaluations.DoesNotExist:
        return None


def all_evaluations():
    """get all evaluations"""
    return Evaluations.objects.all()


def get_user_evaluation_by_id(id: str) -> UserEvaluations:
    """get user evaluation by id"""
    try:
        return UserEvaluations.objects.get(id=int(id))
    except UserEvaluations.DoesNotExist:
        return None


def filter_all_evaluations_based_on_user_and_year(
    user: User, year: int
) -> UserEvaluations:
    """A helper function to filter all user evaluations based on his id."""
    return UserEvaluations.objects.filter(user=user, created_at__year=year)


def all_user_evaluations():
    """get all user evaluations"""
    return UserEvaluations.objects.all()
