from django.urls import path
from cshr.views.company_properties import (
    CompanyPropertiesApiView,
    BaseCompanyPropertiesApiView,
)

urlpatterns = [
    path("", BaseCompanyPropertiesApiView.as_view()),
    path("<str:id>/", CompanyPropertiesApiView.as_view()),
]
