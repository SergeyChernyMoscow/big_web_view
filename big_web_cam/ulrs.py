from django.urls import path
from .views import index, by_home, by_camera, other_page, sub_index

urlpatterns = [
    path('<str:page>', other_page, name='other'),
    path('<int:home_id>/', by_home),
    path('camera/<int:camera_id>/', by_camera),
    path('', index, name = 'index'),
    path('video/', sub_index, name = 'sub_index')
]