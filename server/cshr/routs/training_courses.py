from django.urls import path
from server.cshr.views.training_courses import TrainingCoursesAPIView

urlpatterns = [
    path(
        "<str:id>/",
        TrainingCoursesAPIView.as_view(
            {"get": "get_one", "delete": "delete", "put": "put"}
        ),
    ),
    path("", TrainingCoursesAPIView.as_view({"get": "get_all", "post": "post"})),
]
