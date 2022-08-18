from django.urls import path
from server.cshr.views import office

urlpatterns= [
  
    path('all/',office.officeApiView.as_view({'get': 'get_all'})),
    path('<int:id>',office.officeApiView.as_view({'get': 'get_one','put':'put','delete':'delete'})),
    path('',office.officeApiView.as_view({'post': 'post'})),
    
]