from django.urls import path


from server.cshr.views.evaluation import UserEvaluationsAPIView, EvaluationsAPIView 
from server.cshr.views.evaluation import BaseUserEvaluationsAPIView , BaseEvaluationsAPIView

urlpatterns = [
    path("user/" ,BaseUserEvaluationsAPIView.as_view()),
    path("user/<str:id>/" ,UserEvaluationsAPIView.as_view()),
    path("" ,BaseEvaluationsAPIView.as_view()),
    path("<str:id>/" ,EvaluationsAPIView.as_view()),
  
]
