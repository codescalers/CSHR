from server.cshr.models.hr_letters import HrLetters


def get_hrLetter_by_id(id: str) -> HrLetters:
    """Return hr_letter who have the same id"""
    try:
        return HrLetters.objects.get(id=int(id))
    except HrLetters.DoesNotExist:
        return None


def get_all_hrLetters() -> HrLetters:
    """Return all hr letters"""
    return HrLetters.objects.all()
