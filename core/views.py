
def detalle_grupo(request, grupo_id, rol):
    
    """
    Vista 6: muestra un grupo, sus juegos y sus pertenencias.
    Recibe dos parámetros en la URL: grupo_id (entero) y rol (texto).
    Filtra las pertenencias que todavía no tienen fecha de salida.

    SQL aproximado:
    SELECT pertenencia.*, usuario.*, grupo.*
    FROM core_pertenencia AS pertenencia
    INNER JOIN core_usuario AS usuario
        ON usuario.id = pertenencia.usuario_id
    INNER JOIN core_grupo AS grupo
        ON grupo.id = pertenencia.grupo_id
    WHERE pertenencia.grupo_id = %s
        AND pertenencia.fecha_salida IS NULL
        AND (%s = 'todos' OR pertenencia.rol = %s)
    ORDER BY pertenencia.rol, usuario.username;
    """

    grupo = get_object_or_404(
        Grupo.objects.prefetch_related("juegos"),
        pk=grupo_id,
    )

    # Recuperamos las pertenencias activas del grupo.
    # SQL aproximado:
    # SELECT pertenencia.*, usuario.*, grupo.*
    # FROM core_pertenencia AS pertenencia
    # INNER JOIN core_usuario AS usuario
    #     ON usuario.id = pertenencia.usuario_id
    # INNER JOIN core_grupo AS grupo
    #     ON grupo.id = pertenencia.grupo_id
    # WHERE pertenencia.grupo_id = %s
    # AND pertenencia.fecha_salida IS NULL
    # ORDER BY pertenencia.rol, usuario.username;

    pertenencias = (
        Pertenencia.objects
        .filter(
            grupo=grupo,
            fecha_salida__isnull=True,
        )
        .select_related("usuario", "grupo")
        .order_by("rol", "usuario__username")
    )

    # Si se indica un rol distinto de "todos", filtramos por ese rol.
    if rol != "todos":
        pertenencias = pertenencias.filter(rol=rol)

    # SQL aproximado:
    # SELECT 1
    # FROM core_pertenencia
    # WHERE grupo_id = %s
    # AND fecha_salida IS NULL
    # LIMIT 1;

    # Si el rol escrito no existe, mostramos todas las pertenencias
    # activas para que la página no aparezca vacía.
    if not pertenencias.exists():
        pertenencias = (
            Pertenencia.objects
            .filter(
                grupo=grupo,
                fecha_salida__isnull=True,
            )
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
