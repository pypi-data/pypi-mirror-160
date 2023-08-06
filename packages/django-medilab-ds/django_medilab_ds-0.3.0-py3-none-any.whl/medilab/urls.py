from django.urls import path
from . import views

app_name = 'medilab'

urlpatterns = [
    path('', views.home, name='home'),
]
