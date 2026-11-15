
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Sum, Q

from .models import Usuario, Juego, Grupo, Pertenencia, Noticia


# ============================================================
# VISTA 1: PÁGINA PRINCIPAL
# ============================================================

def index(request):
    """
    Muestra la página principal y los enlaces a las URLs.
    """
    return render(request, "core/index.html")


# ============================================================
# VISTA 2: LISTADO DE USUARIOS
# ============================================================

def lista_usuarios(request):

    # SQL principal aproximado:
    # SELECT usuario.*, perfil.*, configuracion.*, estadisticas.*
    # FROM core_usuario AS usuario
    # LEFT JOIN core_perfilusuario AS perfil
    #     ON perfil.usuario_id = usuario.id
    # LEFT JOIN core_configuracionusuario AS configuracion
    #     ON configuracion.usuario_id = usuario.id
    # LEFT JOIN core_estadisticasusuario AS estadisticas
    #     ON estadisticas.usuario_id = usuario.id
    # ORDER BY usuario.username
    # LIMIT 50;
    #
    # select_related() obtiene las relaciones OneToOne mediante JOIN.
    #
    # Consultas adicionales aproximadas de prefetch_related():
    # SELECT * FROM core_amistad
    # WHERE usuario_origen_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);
    #
    # SELECT * FROM core_amistad
    # WHERE usuario_destino_id IN (...);
    #
    # SELECT grupo.*, pertenencia.usuario_id
    # FROM core_grupo AS grupo
    # INNER JOIN core_pertenencia AS pertenencia
    #     ON grupo.id = pertenencia.grupo_id
    # WHERE pertenencia.usuario_id IN (...);
    #
    # SELECT * FROM core_chat
    # INNER JOIN core_participantechat
    #     ON core_chat.id = core_participantechat.chat_id
    # WHERE core_participantechat.usuario_id IN (...);

    usuarios = (
        Usuario.objects
        .select_related(
            "perfil",
            "configuracion",
            "estadisticas",
        )
        .prefetch_related(
            "amistades_enviadas__usuario_destino",
            "amistades_recibidas__usuario_origen",
            "grupos",
            "chats",
        )
        .order_by("username")[:50]
    )

    return render(
        request,
        "core/usuarios.html",
        {"usuarios": usuarios},
    )


# ============================================================
# VISTA 3: DETALLE DE USUARIO
# ============================================================

def detalle_usuario(request, usuario_id):

    # SQL principal aproximado:
    # SELECT usuario.*, perfil.*, configuracion.*, estadisticas.*
    # FROM core_usuario AS usuario
    # LEFT JOIN core_perfilusuario AS perfil
    #     ON perfil.usuario_id = usuario.id
    # LEFT JOIN core_configuracionusuario AS configuracion
    #     ON configuracion.usuario_id = usuario.id
    # LEFT JOIN core_estadisticasusuario AS estadisticas
    #     ON estadisticas.usuario_id = usuario.id
    # WHERE usuario.id = %s
    # LIMIT 1;
    #
    # Consultas adicionales de prefetch_related():
    # SELECT * FROM core_amistad
    # WHERE usuario_origen_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);
    #
    # SELECT * FROM core_amistad
    # WHERE usuario_destino_id IN (...);
    #
    # SELECT grupo.*, pertenencia.usuario_id
    # FROM core_grupo AS grupo
    # INNER JOIN core_pertenencia AS pertenencia
    #     ON grupo.id = pertenencia.grupo_id
    # WHERE pertenencia.usuario_id IN (...);
    #
    # SELECT usuariojuego.*, juego.*
    # FROM core_usuariojuego AS usuariojuego
    # INNER JOIN core_juego AS juego
    #     ON juego.id = usuariojuego.juego_id
    # WHERE usuariojuego.usuario_id IN (...);
    #
    # SELECT * FROM core_noticia
    # WHERE autor_id IN (...);
    #
    # SELECT * FROM core_comentario
    # WHERE usuario_id IN (...);
    #
    # SELECT * FROM core_noticia
    # WHERE id IN (...);
    #
    # SELECT * FROM core_reaccion
    # WHERE usuario_id IN (...);
    #
    # SELECT * FROM core_notificacion
    # WHERE usuario_id IN (...);
    #
    # SELECT chat.*, participantechat.*, usuario.*
    # FROM core_chat AS chat
    # INNER JOIN core_participantechat AS participantechat
    #     ON chat.id = participantechat.chat_id
    # INNER JOIN core_usuario AS usuario
    #     ON usuario.id = participantechat.usuario_id
    # WHERE chat.id IN (...);
    #
    # SELECT * FROM core_mensaje
    # WHERE autor_id IN (...);

    usuario = get_object_or_404(
        Usuario.objects
        .select_related(
            "perfil",
            "configuracion",
            "estadisticas",
        )
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

    return render(
        request,
        "core/usuario_detalle.html",
        {"usuario": usuario},
    )


# ============================================================
# VISTA 4: LISTADO DE JUEGOS
# ============================================================

def lista_juegos(request):

    # SQL principal aproximado:
    # SELECT juego.*
    # FROM core_juego AS juego
    # WHERE juego.nombre IS NOT NULL
    #   AND juego.genero IS NOT NULL
    #   AND NOT (juego.nombre = '')
    # ORDER BY juego.nombre
    # LIMIT 100;
    #
    # Consultas adicionales de prefetch_related():
    # SELECT grupo.*, pertenencia.grupo_id
    # FROM core_grupo AS grupo
    # INNER JOIN core_grupo_juegos
    #     ON grupo.id = core_grupo_juegos.grupo_id
    # INNER JOIN core_pertenencia AS pertenencia
    #     ON grupo.id = pertenencia.grupo_id
    # WHERE core_grupo_juegos.juego_id IN (...);
    #
    # SELECT * FROM core_usuariojuego
    # WHERE juego_id IN (...);
    #
    # SELECT * FROM core_noticia
    # WHERE juego_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);

    juegos = (
        Juego.objects
        .filter(
            nombre__isnull=False,
            genero__isnull=False,
        )
        .exclude(nombre="")
        .prefetch_related(
            "grupos",
            "usuariojuego_set__usuario",
            "noticia_set__autor",
        )
        .order_by("nombre")[:100]
    )

    return render(
        request,
        "core/juegos.html",
        {"juegos": juegos},
    )


# ============================================================
# VISTA 5: LISTADO DE GRUPOS
# ============================================================

def lista_grupos(request):

    # SQL principal aproximado:
    # SELECT grupo.*
    # FROM core_grupo AS grupo
    # ORDER BY grupo.nombre
    # LIMIT 100;
    #
    # Consultas adicionales de prefetch_related():
    # SELECT usuario.*, pertenencia.grupo_id
    # FROM core_usuario AS usuario
    # INNER JOIN core_pertenencia AS pertenencia
    #     ON usuario.id = pertenencia.usuario_id
    # WHERE pertenencia.grupo_id IN (...);
    #
    # SELECT juego.*, grupo_juegos.grupo_id
    # FROM core_juego AS juego
    # INNER JOIN core_grupo_juegos AS grupo_juegos
    #     ON juego.id = grupo_juegos.juego_id
    # WHERE grupo_juegos.grupo_id IN (...);
    #
    # SELECT * FROM core_pertenencia
    # WHERE grupo_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);

    grupos = (
        Grupo.objects
        .prefetch_related(
            "usuarios",
            "juegos",
            "pertenencia_set__usuario",
        )
        .order_by("nombre")[:100]
    )

    return render(
        request,
        "core/grupos.html",
        {"grupos": grupos},
    )


# ============================================================
# VISTA 6: DETALLE DE GRUPO
# ============================================================

def detalle_grupo(request, grupo_id, rol):

    # SQL principal aproximado:
    # SELECT grupo.*
    # FROM core_grupo AS grupo
    # WHERE grupo.id = %s
    # LIMIT 1;
    #
    # Consulta adicional de prefetch_related():
    # SELECT juego.*, grupo_juegos.grupo_id
    # FROM core_juego AS juego
    # INNER JOIN core_grupo_juegos AS grupo_juegos
    #     ON juego.id = grupo_juegos.juego_id
    # WHERE grupo_juegos.grupo_id IN (...);

    grupo = get_object_or_404(
        Grupo.objects.prefetch_related("juegos"),
        pk=grupo_id,
    )

    # SQL aproximado:
    # SELECT pertenencia.*, usuario.*, grupo.*
    # FROM core_pertenencia AS pertenencia
    # INNER JOIN core_usuario AS usuario
    #     ON usuario.id = pertenencia.usuario_id
    # INNER JOIN core_grupo AS grupo
    #     ON grupo.id = pertenencia.grupo_id
    # WHERE pertenencia.grupo_id = %s
    #   AND pertenencia.fecha_salida IS NULL
    # ORDER BY pertenencia.rol, usuario.username;

    # Recuperamos las pertenencias activas del grupo.
    pertenencias = (
        Pertenencia.objects
        .filter(
            grupo=grupo,
            fecha_salida__isnull=True,
        )
        .select_related(
            "usuario",
            "grupo",
        )
        .order_by(
            "rol",
            "usuario__username",
        )
    )

    if rol != "todos":

        # SQL aproximado:
        # SELECT pertenencia.*, usuario.*, grupo.*
        # FROM core_pertenencia AS pertenencia
        # INNER JOIN core_usuario AS usuario
        #     ON usuario.id = pertenencia.usuario_id
        # INNER JOIN core_grupo AS grupo
        #     ON grupo.id = pertenencia.grupo_id
        # WHERE pertenencia.grupo_id = %s
        #   AND pertenencia.fecha_salida IS NULL
        #   AND pertenencia.rol = %s
        # ORDER BY pertenencia.rol, usuario.username;

        pertenencias = pertenencias.filter(rol=rol)

    # exists() comprueba si hay resultados.
    # SQL aproximado:
    # SELECT 1
    # FROM core_pertenencia
    # WHERE grupo_id = %s
    #   AND fecha_salida IS NULL
    # LIMIT 1;

    if not pertenencias.exists():

        # Si no hay resultados para el rol indicado,
        # se recuperan todas las pertenencias activas del grupo.
        #
        # SQL aproximado:
        # SELECT pertenencia.*, usuario.*, grupo.*
        # FROM core_pertenencia AS pertenencia
        # INNER JOIN core_usuario AS usuario
        #     ON usuario.id = pertenencia.usuario_id
        # INNER JOIN core_grupo AS grupo
        #     ON grupo.id = pertenencia.grupo_id
        # WHERE pertenencia.grupo_id = %s
        #   AND pertenencia.fecha_salida IS NULL
        # ORDER BY pertenencia.rol, usuario.username;

        pertenencias = (
            Pertenencia.objects
            .filter(
                grupo=grupo,
                fecha_salida__isnull=True,
            )
            .select_related(
                "usuario",
                "grupo",
            )
            .order_by(
                "rol",
                "usuario__username",
            )
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


# ============================================================
# VISTA 7: LISTADO DE NOTICIAS
# ============================================================

def lista_noticias(request):

    # SQL principal aproximado:
    # SELECT noticia.*, usuario.*, grupo.*, juego.*
    # FROM core_noticia AS noticia
    # INNER JOIN core_usuario AS usuario
    #     ON usuario.id = noticia.autor_id
    # LEFT JOIN core_grupo AS grupo
    #     ON grupo.id = noticia.grupo_id
    # INNER JOIN core_juego AS juego
    #     ON juego.id = noticia.juego_id
    # ORDER BY noticia.fecha_publicacion DESC
    # LIMIT 50;
    #
    # Consultas adicionales de prefetch_related():
    # SELECT * FROM core_comentario
    # WHERE noticia_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);
    #
    # SELECT * FROM core_reaccion
    # WHERE noticia_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);

    noticias = (
        Noticia.objects
        .select_related(
            "autor",
            "grupo",
            "juego",
        )
        .prefetch_related(
            "comentarios__usuario",
            "reaccion_set__usuario",
        )
        .order_by("-fecha_publicacion")[:50]
    )

    return render(
        request,
        "core/noticias.html",
        {"noticias": noticias},
    )


# ============================================================
# VISTA 8: DETALLE DE NOTICIA
# ============================================================

def detalle_noticia(request, noticia_id):

    # SQL principal aproximado:
    # SELECT noticia.*, usuario.*, grupo.*, juego.*
    # FROM core_noticia AS noticia
    # INNER JOIN core_usuario AS usuario
    #     ON usuario.id = noticia.autor_id
    # LEFT JOIN core_grupo AS grupo
    #     ON grupo.id = noticia.grupo_id
    # INNER JOIN core_juego AS juego
    #     ON juego.id = noticia.juego_id
    # WHERE noticia.id = %s
    # LIMIT 1;
    #
    # Consultas adicionales de prefetch_related():
    # SELECT * FROM core_comentario
    # WHERE noticia_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);
    #
    # SELECT * FROM core_reaccion
    # WHERE noticia_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);

    noticia = get_object_or_404(
        Noticia.objects
        .select_related(
            "autor",
            "grupo",
            "juego",
        )
        .prefetch_related(
            "comentarios__usuario",
            "reaccion_set__usuario",
        ),
        pk=noticia_id,
    )

    return render(
        request,
        "core/noticia_detalle.html",
        {"noticia": noticia},
    )


# ============================================================
# VISTA 9: ESTADÍSTICAS
# ============================================================

def estadisticas(request):

    # SQL aproximado de aggregate():
    # SELECT
    #     COUNT(core_usuario.id) AS total_usuarios,
    #     AVG(core_estadisticasusuario.horas_totales) AS media_horas,
    #     SUM(core_estadisticasusuario.horas_totales) AS total_horas
    # FROM core_usuario
    # LEFT JOIN core_estadisticasusuario
    #     ON core_usuario.id = core_estadisticasusuario.usuario_id;
    #
    # aggregate() ejecuta la consulta y devuelve un diccionario
    # con los resultados calculados directamente en la base de datos.

    resumen = Usuario.objects.aggregate(
        total_usuarios=Count("id"),
        media_horas=Avg("estadisticas__horas_totales"),
        total_horas=Sum("estadisticas__horas_totales"),
    )

    # SQL aproximado:
    # SELECT
    #     usuario.*,
    #     COUNT(noticia.id) AS num_noticias
    # FROM core_usuario AS usuario
    # LEFT JOIN core_noticia AS noticia
    #     ON usuario.id = noticia.autor_id
    # GROUP BY usuario.id
    # HAVING COUNT(noticia.id) >= 1
    # ORDER BY num_noticias DESC, usuario.username
    # LIMIT 20;

    usuarios_con_noticias = (
        Usuario.objects
        .annotate(
            num_noticias=Count("noticia"),
        )
        .filter(num_noticias__gte=1)
        .order_by(
            "-num_noticias",
            "username",
        )[:20]
    )

    return render(
        request,
        "core/estadisticas.html",
        {
            "resumen": resumen,
            "usuarios_con_noticias": usuarios_con_noticias,
        },
    )


# ============================================================
# VISTA 10: BÚSQUEDA DE JUEGOS
# ============================================================

def buscar_juego(request, termino):

    # SQL principal aproximado:
    # SELECT juego.*
    # FROM core_juego AS juego
    # WHERE (
    #     juego.nombre LIKE %s
    #     OR juego.genero LIKE %s
    #     OR juego.descripcion LIKE %s
    # )
    # AND NOT (juego.nombre = '')
    # ORDER BY juego.nombre
    # LIMIT 50;
    #
    # Consultas adicionales de prefetch_related():
    # SELECT * FROM core_grupo_juegos
    # WHERE juego_id IN (...);
    #
    # SELECT * FROM core_usuariojuego
    # WHERE juego_id IN (...);
    #
    # SELECT * FROM core_usuario
    # WHERE id IN (...);

    juegos = (
        Juego.objects
        .filter(
            Q(nombre__icontains=termino)
            | Q(genero__icontains=termino)
            | Q(descripcion__icontains=termino)
        )
        .exclude(nombre="")
        .prefetch_related(
            "grupos",
            "usuariojuego_set__usuario",
        )
        .order_by("nombre")[:50]
    )

    # SQL aproximado de exists():
    # SELECT 1
    # FROM core_juego
    # WHERE (
    #     nombre LIKE %s
    #     OR genero LIKE %s
    #     OR descripcion LIKE %s
    # )
    # AND NOT (nombre = '')
    # LIMIT 1;

    sin_coincidencias = not juegos.exists()

    if sin_coincidencias:

        # Si no hay coincidencias, se muestran los primeros
        # diez juegos disponibles.
        #
        # SQL aproximado:
        # SELECT *
        # FROM core_juego
        # WHERE NOT (nombre = '')
        # ORDER BY nombre
        # LIMIT 10;

        # Consultas adicionales:
        # SELECT * FROM core_grupo_juegos
        # WHERE juego_id IN (...);
        #
        # SELECT * FROM core_usuariojuego
        # WHERE juego_id IN (...);
        #
        # SELECT * FROM core_usuario
        # WHERE id IN (...);

        juegos = (
            Juego.objects
            .exclude(nombre="")
            .prefetch_related(
                "grupos",
                "usuariojuego_set__usuario",
            )
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


# ============================================================
# MANEJADORES DE ERRORES PERSONALIZADOS
# ============================================================

def error_400(request, exception=None):
    return render(
        request,
        "core/errores/400.html",
        status=400,
    )


def error_403(request, exception=None):
    return render(
        request,
        "core/errores/403.html",
        status=403,
    )


def error_404(request, exception=None):
    return render(
        request,
        "core/errores/404.html",
        status=404,
    )


def error_500(request):
    return render(
        request,
        "core/errores/500.html",
        status=500,
    )
