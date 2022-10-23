from django.urls import path
from server.cshr.views.official_documents import (
    OffcialDocumentAPIView,
    OfficialDocumentAcceptApiView,
    OfficialDocumentRejectApiView
)


urlpatterns = [
    path("", OffcialDocumentAPIView.as_view()),
    path("approve/<str:id>/", OfficialDocumentAcceptApiView.as_view()),
    path("reject/<str:id>/", OfficialDocumentRejectApiView.as_view()),

]
