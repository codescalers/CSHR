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
            {"get": "get", "put": "put", "delete": "delete"}, name="evaluation-byId"
        ),
    ),
]
