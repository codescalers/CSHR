from django.urls import path

from server.cshr.views.training_courses import TrainingCoursesApiView , BaseTrainingCoursesApiView

urlpatterns = [
    path("", BaseTrainingCoursesApiView.as_view()),
    path("<str:id>/", TrainingCoursesApiView.as_view()),
]
