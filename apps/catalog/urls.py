from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("katalog/", views.panel_list, name="list"),
    path("katalog/aksessuarlar/", views.accessories, name="accessories"),
    path("katalog/<str:code>/", views.detail, name="detail"),
]
