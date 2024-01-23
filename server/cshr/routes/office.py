from django.urls import path


from cshr.views.office import OfficeApiView, BaseOfficeApiView

urlpatterns = [
    path("", BaseOfficeApiView.as_view()),
    path("<str:id>/", OfficeApiView.as_view()),
]
