"""methods that will serve evaluation endpoints"""
from server.cshr.models.evaluations import UserEvaluations, Evaluations


def get_evaluation_by_id(id: str) -> Evaluations:
    '''get evaluation by id'''
    try:
        return Evaluations.objects.get(id=int(id))
    except UserEvaluations.DoesNotExist:
        return None


def all_evaluations():
    '''get all evaluations'''
    return Evaluations.objects.all()


def get_user_evaluation_by_id(id: str) -> UserEvaluations:
    '''get user evaluation by id'''
    try:
        return UserEvaluations.objects.get(id=int(id))
    except UserEvaluations.DoesNotExist:
        return None


def all_user_evaluations():
    '''get all user evaluations'''
    return UserEvaluations.objects.all()
    
