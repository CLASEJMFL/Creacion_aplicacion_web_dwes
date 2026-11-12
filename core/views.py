
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Sum, Q

from .models import Usuario, Juego, Grupo, Pertenencia, Noticia


# Create your views here.


def index(request):
    """
    Vista 1: muestra la página principal y los enlaces a las diez URLs.
    """
    return render(request, "core/index.html")


def lista_usuarios(request):
    """
    Vista 2: muestra usuarios junto con sus relaciones OneToOne,
    amistades, grupos y chats.
    
    SQL aproximado:
    SELECT usuario.*, perfilusuario.*, configuracionusuario.*,
           estadisticasusuario.*
    FROM core_usuario AS usuario
    LEFT JOIN core_perfilusuario AS perfilusuario
        ON perfilusuario.usuario_id = usuario.id
    LEFT JOIN core_configuracionusuario AS configuracionusuario
        ON configuracionusuario.usuario_id = usuario.id
    LEFT JOIN core_estadisticasusuario AS estadisticasusuario
        ON estadisticasusuario.usuario_id = usuario.id
    ORDER BY usuario.username
    LIMIT 50;
    """
    usuarios = (
        Usuario.objects
        .select_related("perfil", "configuracion", "estadisticas")
        .prefetch_related(
            "amistades_enviadas__usuario_destino",
            "amistades_recibidas__usuario_origen",
            "grupos",
            "chats",
        )
        .order_by("username")[:50]
    )

    return render(request, "core/usuarios.html", {"usuarios": usuarios})


def detalle_usuario(request, usuario_id):
    """
    Vista 3: muestra un usuario y sus relaciones.
    """
    usuario = get_object_or_404(
        Usuario.objects
        .select_related("perfil", "configuracion", "estadisticas")
        .prefetch_related(
            "amistades_enviadas__usuario_destino",
            "amistades_recibidas__usuario_origen",
            "grupos",
            "usuariojuego_set__juego",
            "noticia_set__juego",
            "noticia_set__grupo",
            "comentario_set__noticia",
            "reaccion_set__noticia",
            "notificacion_set",
            "chats__participantechat_set__usuario",
            "mensaje_set__chat",
        ),
        pk=usuario_id,
    )

    return render(request, "core/usuario_detalle.html", {"usuario": usuario})


def lista_juegos(request):
    """
    Vista 4: muestra juegos y sus relaciones ManyToMany
    y relaciones inversas.

    SQL aproximado:
    SELECT juego.*
    FROM core_juego AS juego
    WHERE juego.nombre IS NOT NULL AND juego.genero IS NOT NULL
    ORDER BY juego.nombre
    LIMIT 100;
    """
    juegos = (
        Juego.objects
        .filter(nombre__isnull=False, genero__isnull=False)
        .exclude(nombre="")
        .prefetch_related(
            "grupos",
            "usuariojuego_set__usuario",
            "noticia_set__autor",
        )
        .order_by("nombre")[:100]
    )

    return render(request, "core/juegos.html", {"juegos": juegos})


def lista_grupos(request):
    """
    Vista 5: muestra grupos con usuarios, juegos y pertenencias.

    SQL aproximado:
    SELECT grupo.*
    FROM core_grupo AS grupo
    ORDER BY grupo.nombre
    LIMIT 100;
    """
    grupos = (
        Grupo.objects
        .prefetch_related(
            "usuarios",
            "juegos",
            "pertenencia_set__usuario",
        )
        .order_by("nombre")[:100]
    )

    return render(request, "core/grupos.html", {"grupos": grupos})


def detalle_grupo(request, grupo_id, rol):
    """
    Vista 6: muestra un grupo, sus juegos y sus pertenencias,
    filtradas por rol y fecha de unión.

    SQL aproximado:
    SELECT pertenencia.*, usuario.*
    FROM core_pertenencia AS pertenencia
    INNER JOIN core_usuario AS usuario
        ON usuario.id = pertenencia.usuario_id
    WHERE pertenencia.grupo_id = %s
      AND pertenencia.fecha_union IS NOT NULL
    ORDER BY pertenencia.rol, usuario.username;
    """
    grupo = get_object_or_404(
        Grupo.objects.prefetch_related("juegos"),
        pk=grupo_id,
    )

    pertenencias = (
        Pertenencia.objects
        .filter(grupo=grupo, fecha_union__isnull=False)
        .select_related("usuario", "grupo")
        .order_by("rol", "usuario__username")
    )

    if rol != "todos":
        pertenencias = pertenencias.filter(rol=rol)

    if not pertenencias.exists():
        pertenencias = (
            Pertenencia.objects
            .filter(grupo=grupo, fecha_union__isnull=False)
            .select_related("usuario", "grupo")
            .order_by("rol", "usuario__username")
        )
        rol_no_encontrado = rol != "todos"
    else:
        rol_no_encontrado = False

    return render(
        request,
        "core/grupo_detalle.html",
        {
            "grupo": grupo,
            "pertenencias": pertenencias,
            "rol": rol,
            "rol_no_encontrado": rol_no_encontrado,
        },
    )


def lista_noticias(request):
    """
    Vista 7: muestra noticias con autor, grupo, juego,
    comentarios y reacciones.

    SQL aproximado:
    SELECT noticia.*, usuario.*, grupo.*, juego.*
    FROM core_noticia AS noticia
    INNER JOIN core_usuario AS usuario ON usuario.id = noticia.autor_id
    LEFT JOIN core_grupo AS grupo ON grupo.id = noticia.grupo_id
    INNER JOIN core_juego AS juego ON juego.id = noticia.juego_id
    ORDER BY noticia.fecha_publicacion DESC
    LIMIT 50;
    """
    noticias = (
        Noticia.objects
        .select_related("autor", "grupo", "juego")
        .prefetch_related(
            "comentarios__usuario",
            "reaccion_set__usuario",
        )
        .order_by("-fecha_publicacion")[:50]
    )

    return render(request, "core/noticias.html", {"noticias": noticias})


def detalle_noticia(request, noticia_id):
    """
    Vista 8: muestra una noticia concreta con todas sus relaciones.
    """
    noticia = get_object_or_404(
        Noticia.objects
        .select_related("autor", "grupo", "juego")
        .prefetch_related(
            "comentarios__usuario",
            "reaccion_set__usuario",
        ),
        pk=noticia_id,
    )

    return render(request, "core/noticia_detalle.html", {"noticia": noticia})


def estadisticas(request):
    """
    Vista 9: calcula agregaciones y filtra usuarios por
    el número de noticias publicadas.

    SQL aproximado:
    SELECT COUNT(core_usuario.id),
           AVG(core_estadisticasusuario.horas_totales),
           SUM(core_estadisticasusuario.horas_totales)
    FROM core_usuario
    LEFT JOIN core_estadisticasusuario
        ON core_estadisticasusuario.usuario_id = core_usuario.id;

    SQL aproximado del filtro de agregación:
    SELECT usuario.*, COUNT(noticia.id) AS num_noticias
    FROM core_usuario AS usuario
    LEFT JOIN core_noticia AS noticia
        ON noticia.autor_id = usuario.id
    GROUP BY usuario.id
    HAVING COUNT(noticia.id) >= 1
    ORDER BY num_noticias DESC, usuario.username;
    """
    resumen = Usuario.objects.aggregate(
        total_usuarios=Count("id"),
        media_horas=Avg("estadisticas__horas_totales"),
        total_horas=Sum("estadisticas__horas_totales"),
    )

    usuarios_con_noticias = (
        Usuario.objects
        .annotate(num_noticias=Count("noticia"))
        .filter(num_noticias__gte=1)
        .order_by("-num_noticias", "username")[:20]
    )

    return render(
        request,
        "core/estadisticas.html",
        {
            "resumen": resumen,
            "usuarios_con_noticias": usuarios_con_noticias,
        },
    )


def buscar_juego(request, termino):
    """
    Vista 10: busca juegos por nombre, género o descripción.

    SQL aproximado:
    SELECT juego.*
    FROM core_juego AS juego
    WHERE (
        juego.nombre LIKE %s OR
        juego.genero LIKE %s OR
        juego.descripcion LIKE %s
    )
    AND NOT (juego.nombre = '')
    ORDER BY juego.nombre
    LIMIT 50;
    """
    juegos = (
        Juego.objects
        .filter(
            Q(nombre__icontains=termino)
            | Q(genero__icontains=termino)
            | Q(descripcion__icontains=termino)
        )
        .exclude(nombre="")
        .prefetch_related("grupos", "usuariojuego_set__usuario")
        .order_by("nombre")[:50]
    )

    sin_coincidencias = not juegos.exists()

    if sin_coincidencias:
        juegos = (
            Juego.objects
            .exclude(nombre="")
            .prefetch_related("grupos", "usuariojuego_set__usuario")
            .order_by("nombre")[:10]
        )

    return render(
        request,
        "core/buscar_juego.html",
        {
            "juegos": juegos,
            "termino": termino,
            "sin_coincidencias": sin_coincidencias,
        },
    )


# Errores personalizados

def error_400(request, exception=None):
    return render(request, "core/errores/400.html", status=400)


def error_403(request, exception=None):
    return render(request, "core/errores/403.html", status=403)


def error_404(request, exception=None):
    return render(request, "core/errores/404.html", status=404)


def error_500(request, exception=None):
    return render(request, "core/errores/500.html", status=500)