from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('test', views.second_index, name = 'second_index'),
    path('selection', views.process_user_input, name = 'process_input' )
]