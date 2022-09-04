from django.urls import path


from server.cshr.views.userEvaluation import EvaluationsAPIView

urlpatterns = [
    path(
        "user/",
        EvaluationsAPIView.as_view({"get": "get_all", "post": "post"}),
        name="evaluation",
    ),
    path(
        "user/<str:id>/",
        EvaluationsAPIView.as_view(
            {"get": "get", "patch": "patch", "delete": "delete"}, name="evaluation-byId"
        ),
    ),
]
