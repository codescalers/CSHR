from django.urls import path


from server.cshr.views.evaluation import UserEvaluationsAPIView

urlpatterns = [
    path(
        "user/",
        UserEvaluationsAPIView.as_view({"get": "get_all", "post": "post"}),
        name="evaluation",
    ),
    path(
        "user/<str:id>/",
        UserEvaluationsAPIView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}, name="evaluation-byId"
        ),
    ),
]
