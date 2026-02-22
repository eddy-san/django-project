from django.urls import path
from apps.home.presentation import views

urlpatterns = [
    path("", views.index, name="home"),
]