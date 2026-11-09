from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("mahsulot-haqida/", views.about, name="about"),
    path("aloqa/", views.contact, name="contact"),
]
