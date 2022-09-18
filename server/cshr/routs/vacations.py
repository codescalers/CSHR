from django.urls import path
from server.cshr.views.vacations import (
    VacationApprovalAPIView,
    VacationCommentsAPIView,
    VacationsApiView,
    VacationsUpdateApiView,
)


urlpatterns = [
     path("", VacationsApiView.as_view({"get": "get_all", "post": "post"})),
     path("<str:id>/", VacationsApiView.as_view({"get": "get_one", "delete": "delete"})),
     path(
        "edit/<str:id>/",
        VacationsUpdateApiView.as_view(
            {
                "put": "put",
            }
        ),
     ),
     path("put/<str:id>/", VacationApprovalAPIView.as_view()),
     path("comment/<str:id>/", VacationCommentsAPIView.as_view()),
    ]
