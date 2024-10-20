from django.urls import path


from cshr.views.evaluation import UserEvaluationsAPIView, EvaluationsAPIView
from cshr.views.evaluation import (
    BaseUserEvaluationsAPIView,
    BaseEvaluationsAPIView,
)

urlpatterns = [
    path("", BaseEvaluationsAPIView.as_view()),
    path("users/", BaseUserEvaluationsAPIView.as_view()),
    path("<str:id>/", EvaluationsAPIView.as_view()),
    path("user/<str:id>/", UserEvaluationsAPIView.as_view()),
]
