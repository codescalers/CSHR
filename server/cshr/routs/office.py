from django.urls import path
from server.cshr.views import office

from server.cshr.views.office import  OfficeAPIView
 
urlpatterns = [
 path('', OfficeAPIView.as_view({'get': 'get_all', 'post': 'post'})),
 path('<str:id>/', OfficeAPIView.as_view({'get': 'get_one', 'put':'put', 'delete':'delete'}))
 
]