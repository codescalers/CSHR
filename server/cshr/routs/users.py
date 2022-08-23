from django.urls import path
 
from server.cshr.views.users import (GeneralUserAPIView, SupervisorUserAPIView,
 AdminUserAPIView )


urlpatterns = [
    path("admin/<str:id>/", AdminUserAPIView.as_view({
        'get': 'get_one',
        'delete': 'delete',
        'put':'put'
    }) ),
    path("", GeneralUserAPIView.as_view({'get':'get_all'})),
    path("<str:id>/",GeneralUserAPIView.as_view({'get':'get_one'})),

    path("supervisor/<str:id>/", SupervisorUserAPIView.as_view({'get':'get_one'})),
    path("supervisor/", SupervisorUserAPIView.as_view({'get':'get_all'})),
    path("admin/", AdminUserAPIView.as_view({'get':'get_all'})),

   
     
    
]
