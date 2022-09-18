from django.urls import path


from server.cshr.views.office import OfficeApiView , BaseOfficeApiView

urlpatterns = [
    path("", BaseOfficeApiView.as_view()),
    path("<str:id>/", OfficeApiView.as_view()),
]
