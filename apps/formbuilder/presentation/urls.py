from django.urls import path
from .views import fill_form

urlpatterns = [
    path("f/<slug:slug>/", fill_form, name="form_fill"),
]