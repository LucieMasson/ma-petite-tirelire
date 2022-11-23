from django.urls import path
from controller.tirelire import views

urlpatterns = [
    path("tirelires", views.list_piggybanks),
    path("tirelires/create", views.create),
    path("tirelires/<int:piggybank_id>/save", views.save),
    path("tirelires/<int:piggybank_id>/shake", views.shake),
    path("tirelires/<int:piggybank_id>/smash", views.smash),
]
