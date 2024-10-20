from django.urls import path


from cshr.views.office import GetOfficePublicHolidaysBasedOnYearAPIView, OfficeApiView, BaseOfficeApiView

urlpatterns = [
    path("", BaseOfficeApiView.as_view()),
    path("holidays/", GetOfficePublicHolidaysBasedOnYearAPIView.as_view()),
    path("<str:id>/", OfficeApiView.as_view()),
]
