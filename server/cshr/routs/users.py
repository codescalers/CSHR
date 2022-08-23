from django.urls import path
from server.cshr.views.users import  GeneralUserAPIView


urlpatterns = [
    # path("<str:id>/", UserAPIView.as_view({
    #     'get': 'get_one',
    #     'delete': 'delete',
    #     'patch': 'patch',
    #     'put':'put'
    # }), name="user"),
    path("", GeneralUserAPIView.as_view({'get':'get_all'})),
    path("<str:id>/",GeneralUserAPIView.as_view({'get':'get_one'}))
    # path("admin/", UserAPIView_Admin.as_view({'get':'get_all'}))
     
    
]
