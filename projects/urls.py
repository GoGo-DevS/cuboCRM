from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.board, name="board"),
    path("nuevo/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/editar/", views.update, name="update"),
    path("<int:pk>/estado/", views.set_estado, name="set_estado"),
    path("<int:pk>/entregable/nuevo/", views.deliverable_create, name="deliverable_create"),
    path("entregable/<int:pk>/estado/", views.deliverable_set_estado, name="deliverable_set_estado"),
    path("entregable/<int:pk>/revision/", views.revision_create, name="revision_create"),
]
