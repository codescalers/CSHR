from server.cshr.models.training_courses import TrainingCourses


def get_training_courses_by_id(id: str) -> TrainingCourses:
    """Return training course who have the same id"""
    try:
        return TrainingCourses.objects.get(id=int(id))
    except TrainingCourses.DoesNotExist:
        return None


def get_all_training_courses() -> TrainingCourses:
    """Return all training courses"""
    return TrainingCourses.objects.all()


def get_training_courses_for_a_user(id: int) -> TrainingCourses:
    """Return all training courses for a specific user"""
    return TrainingCourses.objects.filter(user=id)
