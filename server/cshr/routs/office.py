from django.urls import path


from server.cshr.views.office import OfficeAPIView

urlpatterns = [
    path("", OfficeAPIView.as_view({"post": "post"})),
    path("all/", OfficeAPIView.as_view({"get": "get_all"})),
    path(
        "<str:id>/",
        OfficeAPIView.as_view({"get": "get", "put": "put", "delete": "delete"}),
    ),
]
