from django.urls import path
from ..views.training_courses import TrainingCoursesAPIView
urlpatterns = [
path("<str:id>/", TrainingCoursesAPIView.as_view({
       'get': 'get_one',
       'delete': 'delete',
       'put':'put' })),

      path("all/", TrainingCoursesAPIView.as_view({'get':'get_all'})),
      path("", TrainingCoursesAPIView.as_view({'post':'post'})) ]