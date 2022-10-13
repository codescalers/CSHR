"""   this file will contain functions to make union for all request types """
from server.cshr.services.hr_letters import get_all_hrLetters
from server.cshr.services.vacations import filter_vacations_by_pending_status
from server.cshr.services.compensation import get_all_compensations
from typing import List, Dict
from server.cshr.models.hr_letters import HrLetters
from server.cshr.models.compensation import Compensation
from server.cshr.models.vacations import Vacation
from server.cshr.serializers.vacations import LandingPageVacationsSerializer
from server.cshr.serializers.compensation import LandingPageCompensationSerializer
from server.cshr.serializers.hr_letters import LandingPageHrLetterSerializer


def requests_format_response() -> Dict:
    """will concatnate all objects and send back as obj"""
    vacations: List[Vacation] = LandingPageVacationsSerializer(
        filter_vacations_by_pending_status(), many=True
    ).data
    hr_letters: List[HrLetters] = LandingPageHrLetterSerializer(
        get_all_hrLetters(), many=True
    ).data
    compensations: List[Compensation] = LandingPageCompensationSerializer(
        get_all_compensations(), many=True
    ).data
    response: Dict = {}
    response["vacations"] = vacations
    response["hr_letters"] = hr_letters
    response["compensations"] = compensations
    return response
