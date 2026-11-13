from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 1: página principal
    path(
        "",
        views.index,
        name="index",
    ),

    # URL 2: listado de usuarios
    path(
        "usuarios/",
        views.lista_usuarios,
        name="usuarios",
    ),

    # URL 3: detalle de usuario
    path(
        "usuarios/<int:usuario_id>/",
        views.detalle_usuario,
        name="usuario_detalle",
    ),

    # URL 4: listado de juegos
    path(
        "juegos/",
        views.lista_juegos,
        name="juegos",
    ),

    # URL 5: listado de grupos
    path(
        "grupos/",
        views.lista_grupos,
        name="grupos",
    ),

    # URL 6: detalle de grupo por identificador y rol
    path(
        "grupos/<int:grupo_id>/<str:rol>/",
        views.detalle_grupo,
        name="grupo_detalle",
    ),

    # URL 7: listado de noticias
    path(
        "noticias/",
        views.lista_noticias,
        name="noticias",
    ),

    # URL 8: detalle de noticia
    path(
        "noticias/<int:noticia_id>/",
        views.detalle_noticia,
        name="noticia_detalle",
    ),

    # URL 9: estadísticas
    path(
        "estadisticas/",
        views.estadisticas,
        name="estadisticas",
    ),

    # URL 10: búsqueda de juegos
    path(
        "buscar/<str:termino>/",
        views.buscar_juego,
        name="buscar_juego",
    ),
    
    # Url con re_path
    re_path(
        r'^buscar-regex/(?P<termino>[a-zA-Z0-9_-]+)/$',
        views.buscar_juego,
        name="buscar_juego_regex"
    ),
]
