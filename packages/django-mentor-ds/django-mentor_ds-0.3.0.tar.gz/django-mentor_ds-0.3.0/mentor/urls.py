from django.urls import path
from . import views

app_name = 'mentor'

urlpatterns = [
    path('', views.home, name='home'),
]
