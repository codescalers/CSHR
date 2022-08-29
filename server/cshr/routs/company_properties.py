from django.urls import path
from server.cshr.views.company_properties import CompanyPropertiesAPIView

urlpatterns = [
    path("", CompanyPropertiesAPIView.as_view({"post": "post", "get": "get_all"})),
    path(
        "<str:id>/",
        CompanyPropertiesAPIView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}
        ),
    ),
]