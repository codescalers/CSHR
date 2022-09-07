from django.urls import path


from server.cshr.views.office import OfficeAPIView

urlpatterns = [
    path("", OfficeAPIView.as_view({"get": "get_all", "post": "post"}), name="office"),
    path(
        "<str:id>/",
        OfficeAPIView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}, name="office-id"
        ),
    ),
]
