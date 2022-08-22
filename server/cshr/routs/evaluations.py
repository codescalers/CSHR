from django.urls import path


from server.cshr.views.evaluations import EvaluationAPIView

urlpatterns = [
    path("", EvaluationAPIView.as_view({"post": "post"})),
    path("", EvaluationAPIView.as_view({"get": "get_all"})),
    path(
        "<str:id>/",
        EvaluationAPIView.as_view({"get": "get", "put": "put", "delete": "delete"}),
    ),
]
