"""   this file will contain functions to make union for all request types """
from server.cshr.models.official_documents import OffcialDocument
from server.cshr.serializers.official_documents import OffcialDocumentSerializer
from server.cshr.models.users import USER_TYPE, User
from server.cshr.services.hr_letters import (
    filter_hr_letter_by_pinding_status,
    get_hr_letter_by_user,
)
from server.cshr.services.official_documents import filter_all_official_docs_by_pinding_status
from server.cshr.services.vacations import (
    filter_user_vacations,
    filter_vacations_by_pending_status,
)
from server.cshr.services.compensation import (
    filter_all_compensations_by_pinding_status,
    get_compensations_by_user,
)
from typing import List, Dict
from server.cshr.models.hr_letters import HrLetters
from server.cshr.models.compensation import Compensation
from server.cshr.models.vacations import Vacation
from server.cshr.serializers.vacations import LandingPageVacationsSerializer
from server.cshr.serializers.compensation import LandingPageCompensationSerializer
from server.cshr.serializers.hr_letters import LandingPageHrLetterSerializer


def requests_format_response(user: User) -> Dict:
    """will concatnate all objects and send back as obj"""
    if user.user_type == USER_TYPE.USER:
        # So we have to return only his requests.
        vacations: List[Vacation] = LandingPageVacationsSerializer(
            filter_user_vacations(user), many=True
        ).data
        hr_letters: List[HrLetters] = LandingPageHrLetterSerializer(
            get_hr_letter_by_user(user), many=True
        ).data
        compensations: List[Compensation] = LandingPageCompensationSerializer(
            get_compensations_by_user(user), many=True
        ).data
        official_docs: List[OffcialDocument] = []
    elif user.user_type == USER_TYPE.ADMIN:
        hr_letters: List[HrLetters] = LandingPageHrLetterSerializer(
            filter_hr_letter_by_pinding_status(), many=True
        ).data
        vacations: List[Vacation] = []
        official_docs: List[OffcialDocument] = OffcialDocumentSerializer(
            filter_all_official_docs_by_pinding_status(), many=True
        ).data
        compensations: List[Compensation] = LandingPageCompensationSerializer(
            filter_all_compensations_by_pinding_status(), many=True
        ).data
    else:
        # ==> USER_TYPE.SUPERVISOR
        vacations: List[Vacation] = LandingPageVacationsSerializer(
            filter_vacations_by_pending_status(user), many=True
        ).data
        hr_letters: List[HrLetters] = []
        compensations: List[Compensation] = []
        official_docs: List[OffcialDocument] = []

    response: Dict = {}
    response["vacations"] = vacations[::-1]
    response["hr_letters"] = hr_letters[::-1]
    response["compensations"] = compensations[::-1]
    response["official_docs"] = official_docs[::-1]
    return response
