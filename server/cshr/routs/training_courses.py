from django.urls import path

from server.cshr.views.training_courses import TrainingCoursesApiView

urlpatterns = [
    path("", TrainingCoursesApiView.as_view({"post": "post", "get": "get_all"})),
    path(
        "<str:id>/",
        TrainingCoursesApiView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}
        ),
    ),
]
