from django.urls import path
from server.cshr.views.vacations import (
    BaseVacationsApiView,
    UserVacationBalanceApiView,
    VacationApprovalAPIView,
    VacationCommentsAPIView,
    VacationsAcceptApiView,
    VacationsApiView,
    VacationsRejectApiView,
    VacationsUpdateApiView,
    VacationUserApiView,
    UserVacationBalanceUpdateApiView,
    UserBalanceUpdateApiView,
)

urlpatterns = [
    path("", BaseVacationsApiView.as_view()),
    # path("user/", VacationUserApiView.as_view()),
    # path("edit/<str:id>/", VacationsUpdateApiView.as_view()),
    # path("accept/<str:id>/", VacationsAcceptApiView.as_view()),
    # path("reject/<str:id>/", VacationsRejectApiView.as_view()),
    # path("<str:id>/", VacationsApiView.as_view()),
    # path("put/<str:id>/", VacationApprovalAPIView.as_view()),
    # path("comment/<str:id>/", VacationCommentsAPIView.as_view()),
    path("balance/", UserVacationBalanceApiView.as_view()),
    # path("updatebasebalance", UserVacationBalanceUpdateApiView.as_view()),
    # path("updateuserbalance", UserBalanceUpdateApiView.as_view()),
]
