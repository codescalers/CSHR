from django.urls import path


from server.cshr.views.evaluation import EvaluationsAPIView

urlpatterns = [
    path(
        "",
        EvaluationsAPIView.as_view({"get": "get_all", "post": "post"}),
        name="evaluation",
    ),
    path(
        "<str:id>/",
        EvaluationsAPIView.as_view(
            {"get": "get", "patch": "patch", "delete": "delete"}, name="evaluation-byId"
        ),
    ),
]