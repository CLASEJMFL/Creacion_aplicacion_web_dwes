from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 6: grupo por identificador y rol
    path(
        "grupos/<int:grupo_id>/<str:rol>/",
        views.detalle_grupo,
        name="grupo_detalle",
    ),

    # URL 4: listado de juegos
    path(
        "juegos/",
        views.lista_juegos,
        name="juegos",
    ),
]