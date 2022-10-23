from django.urls import path
from server.cshr.views.official_documents import (
    OffcialDocumentAPIView,
)


urlpatterns = [
    path("", OffcialDocumentAPIView.as_view()),
]