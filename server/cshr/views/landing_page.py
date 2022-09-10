"""This file contains everything related to the landing page functionalty."""
from rest_framework.generics import GenericAPIView
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.api.response import CustomResponse
from typing import Any

from server.cshr.services.landing_page import landing_page_calendar_functionalty


class LandingPageApiView(GenericAPIView):
    permission_classes = (UserIsAuthenticated,)

    def get(self, request):
        month: str = request.query_params.get("month")
        year: str = request.query_params.get("year")
        events: Any = landing_page_calendar_functionalty(month, year)
        return CustomResponse.success(data=events)
