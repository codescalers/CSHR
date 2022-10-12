"""   this file will contain functions to make union for all request types """
from server.cshr.models.requests import Requests
from server.cshr.services.hr_letters import get_all_hrLetters
from server.cshr.services.vacations import filter_vacations_by_pending_status
from typing import List, Dict
from server.cshr.models.hr_letters import HrLetters
from server.cshr.models.vacations import Vacation
from server.cshr.serializers.vacations import LandingPageVacationsSerializer
from server.cshr.serializers.hr_letters import LandingPageHrLetterSerializer


def requests_format_response() -> Dict:
    """will concatnate all objects and send back as obj"""
    vacations: List[Vacation] = LandingPageVacationsSerializer(
        filter_vacations_by_pending_status(), many=True
    ).data
    hr_letters: List[HrLetters] = LandingPageHrLetterSerializer(
        get_all_hrLetters(), many=True
    ).data
    response: Dict = {}
    response["vacations"] = vacations
    response["hr_letters"] = hr_letters
    return response


def get_request_by_id(id: str) -> Requests:
    """Returns a request based on its id"""
    if id.isdigit():
        try:
            return Requests.objects.get(id=int(id))
        except Requests.DoesNotExist:
            return None
    return None