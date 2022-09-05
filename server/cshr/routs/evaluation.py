from django.urls import path


from server.cshr.views.evaluation import UserEvaluationsAPIView, EvaluationsAPIView

urlpatterns = [
    path(
        "user/",
        UserEvaluationsAPIView.as_view({"get": "get_all", "post": "post"}),
        name="UserEvaluation",
    ),
    path(
        "user/<str:id>/",
        UserEvaluationsAPIView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}, name="UserEvaluation-byId"
        ),
    ),
    path(
        "",
        EvaluationsAPIView.as_view({"get": "get_all", "post": "post"}),
        name="evaluation",
    ),
    path(
        "<str:id>/",
        EvaluationsAPIView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}, name="evaluation-byId"
        ),
    ),
]
