from django.urls import path
from server.cshr.views.vacations import (
    BaseVacationsApiView,
    VacationCommentsAPIView,
    VacationsHelpersApiView,
    VacationsUpdateApiView,
    VacationUserApiView,
    VacationsAcceptApiView,
    VacationsRejectApiView,
    UserVacationBalanceApiView,
    PostAdminVacationBalanceApiView,
    GetAdminVacationBalanceApiView,
    CalculateVacationDaysApiView,
    VacationBalanceAdjustmentApiView,
)

urlpatterns = [
    path("", BaseVacationsApiView.as_view()),
    path("user/", VacationUserApiView.as_view()),
    path("calculate/", CalculateVacationDaysApiView.as_view()),
    path("post-admin-balance/", PostAdminVacationBalanceApiView.as_view()),
    path("get-admin-balance/", GetAdminVacationBalanceApiView.as_view()),
    path("balance/adjustment/", VacationBalanceAdjustmentApiView.as_view()),
    path("balance/", UserVacationBalanceApiView.as_view()),
    path("edit/<str:id>/", VacationsUpdateApiView.as_view()),
    path("approve/<str:id>/", VacationsAcceptApiView.as_view()),
    path("reject/<str:id>/", VacationsRejectApiView.as_view()),
    path("<str:id>/", VacationsHelpersApiView.as_view()),
    path("comment/<str:id>/", VacationCommentsAPIView.as_view()),
]
