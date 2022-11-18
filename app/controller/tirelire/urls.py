from django.urls import path
from controller.tirelire import views

urlpatterns = [
    path("tirelires/create", views.create),
    path("tirelires/<int:tirelire_id>/save", views.save),
]
