from django.urls import path

from . import views

app_name = "briefs"

urlpatterns = [
    path("", views.brief_list, name="list"),
    path("nuevo/", views.brief_create, name="create"),
    path("<int:pk>/", views.brief_detail, name="detail"),
    path("<int:pk>/editar/", views.brief_update, name="update"),
]
