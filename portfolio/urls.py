from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.case_list, name="list"),
    path("proyecto/<int:pk>/generar/", views.case_from_project, name="from_project"),
    path("<slug:slug>/", views.case_detail, name="detail"),
    path("<slug:slug>/publicar/", views.case_toggle_publish, name="toggle_publish"),
]
