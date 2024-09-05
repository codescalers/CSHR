"""This file contains everything related to the landing page functionalty."""

from rest_framework.generics import GenericAPIView
from cshr.api.permission import UserIsAuthenticated
from cshr.api.response import CustomResponse
from typing import Any

from cshr.services.landing_page import landing_page_calendar_functionality
from django.core.cache import cache


class LandingPageApiView(GenericAPIView):
    permission_classes = (UserIsAuthenticated,)

    def get(self, request):
        month: str = request.query_params.get("month")
        year: str = request.query_params.get("year")
        
        # Use cache to store results if the same request is made frequently
        cache_key = f"landing_page_{request.user.id}_{month}_{year}"
        events = cache.get(cache_key)
        
        if not events:
            events: Any = landing_page_calendar_functionality(request.user, month, year)
            cache.set(cache_key, events, timeout=60*10)  # Cache for 10 minutes

        return CustomResponse.success(data=events)