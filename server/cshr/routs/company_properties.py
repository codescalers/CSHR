from django.urls import path
from server.cshr.views.company_properties import CompanyPropertiesApiView

urlpatterns = [
    path("", CompanyPropertiesApiView.as_view({"post": "post", "get": "get_all"})),
    path(
        "<str:id>/",
        CompanyPropertiesApiView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}
        ),
    ),
]
