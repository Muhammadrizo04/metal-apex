from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("katalog/<str:code>/", views.detail, name="detail"),
]
