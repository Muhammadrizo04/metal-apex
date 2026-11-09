from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("buyurtma/", views.submit, name="submit"),
    path("buyurtma/qabul/", views.thanks, name="thanks"),
]
