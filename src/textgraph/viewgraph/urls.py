from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.second_index, name = 'second_index'),
    path('action_page.php/', views.process_user_input, name = 'process_input' )
]