from django.urls import path


from cshr.views.office import OfficeApiView, BaseOfficeApiView, OfficeSupervisorsApiView

urlpatterns = [
    path("", BaseOfficeApiView.as_view()),
    path("<str:id>/", OfficeApiView.as_view()),
    path("<str:id>/supervisors/", OfficeSupervisorsApiView.as_view()),
]
