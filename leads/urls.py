from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("", views.board, name="board"),
    path("nuevo/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/editar/", views.update, name="update"),
    path("<int:pk>/eliminar/", views.delete, name="delete"),
    path("<int:pk>/estado/", views.set_estado, name="set_estado"),
    path("<int:pk>/convertir/", views.convert, name="convert"),
]
