# GameLoop

# Creación Aplicación Web Parte I

## 1. Descripción del proyecto

**GameLoop** es una aplicación web desarrollada con Django que permite crear una comunidad de usuarios relacionada con los videojuegos. Incluye perfiles, amistades, grupos, juegos, noticias, comentarios, reacciones, chats, mensajes y notificaciones.

El objetivo es poner en práctica el diseño de modelos, las relaciones entre entidades, la generación de datos de prueba y las copias de seguridad de una aplicación web.

## 2. Tecnologías utilizadas

- **Python 3:** lenguaje de programación.
- **Django:** framework para el desarrollo web.
- **SQLite:** base de datos utilizada en la configuración del proyecto.
- **Faker:** biblioteca para generar datos ficticios de prueba.
- **Git y GitHub:** control de versiones y alojamiento del código.

## 3. Estructura del proyecto

```text
Proyecto_2_DAW/
├── manage.py
├── requirements.txt
├── .gitignore
├── GameLoop/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── core/
    ├── models.py
    ├── admin.py
    ├── views.py
    ├── urls.py
    ├── fixtures/
    │   └── datos.json
    ├── templates/
    │   └── core/
    └── management/
        └── commands/
            └── seed.py
```

- `manage.py`: permite ejecutar comandos de administración de Django.
- `requirements.txt`: contiene las dependencias del proyecto.
- `.gitignore`: excluye archivos locales que no deben incluirse en Git.
- `GameLoop/settings.py`: contiene la configuración del proyecto.
- `GameLoop/urls.py`: define las rutas principales.
- `core/models.py`: contiene los modelos y sus relaciones.
- `core/admin.py`: configura la administración de los modelos.
- `core/views.py`: contiene las vistas de la aplicación.
- `core/urls.py`: define las URLs de la aplicación.
- `core/fixtures/datos.json`: contiene datos de prueba para cargar en la base de datos.
- `core/templates/core/`: contiene las plantillas HTML.
- `core/management/commands/seed.py`: contiene el comando personalizado para generar datos de prueba.

## 4. Modelos de la aplicación

El proyecto cuenta con 16 modelos declarados en `core/models.py`.

### 4.1. Usuario

Hereda de `AbstractUser`, que proporciona campos de autenticación y gestión de cuentas, como `username`, `first_name`, `last_name`, `email` y `password`.

| Campo | Tipo | Parámetros |
|---|---|---|
| `foto_perfil` | `URLField` | `blank=True` |
| `biografia` | `TextField` | `blank=True` |
| `fecha_registro` | `DateTimeField` | `auto_now_add=True` |

Representa a los usuarios registrados en GameLoop.

### 4.2. PerfilUsuario

Almacena información adicional del perfil de cada usuario.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `OneToOneField` | `on_delete=CASCADE`, `related_name="perfil"` |
| `nombre_visible` | `CharField` | `max_length=100`, `blank=True` |
| `biografia` | `TextField` | `blank=True` |
| `fecha_nacimiento` | `DateField` | `null=True`, `blank=True` |
| `web` | `URLField` | `blank=True` |

### 4.3. ConfiguracionUsuario

Guarda las preferencias de cada usuario.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `OneToOneField` | `on_delete=CASCADE`, `related_name="configuracion"` |
| `tema_oscuro` | `BooleanField` | `default=False` |
| `notificaciones_activadas` | `BooleanField` | `default=True` |
| `idioma` | `CharField` | `max_length=10`, `default="es"` |

### 4.4. EstadisticasUsuario

Almacena estadísticas relacionadas con la actividad del usuario.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `OneToOneField` | `on_delete=CASCADE`, `related_name="estadisticas"` |
| `juegos_favoritos` | `PositiveIntegerField` | `default=0` |
| `horas_totales` | `FloatField` | `default=0` |
| `nivel` | `PositiveSmallIntegerField` | `default=1` |
| `puntuacion_media` | `DecimalField` | `max_digits=4`, `decimal_places=2`, `default=0` |

### 4.5. Amistad

Representa las solicitudes y relaciones de amistad entre usuarios.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario_origen` | `ForeignKey` | `on_delete=CASCADE`, `related_name="amistades_enviadas"` |
| `usuario_destino` | `ForeignKey` | `on_delete=CASCADE`, `related_name="amistades_recibidas"` |
| `estado` | `CharField` | `max_length=20`, `default="pendiente"` |
| `fecha_solicitud` | `DateTimeField` | `auto_now_add=True` |
| `fecha_aceptacion` | `DateTimeField` | `null=True`, `blank=True` |

### 4.6. Grupo

Representa comunidades de usuarios relacionadas con videojuegos.

| Campo | Tipo | Parámetros |
|---|---|---|
| `nombre` | `CharField` | `max_length=100` |
| `descripcion` | `TextField` | `blank=True` |
| `imagen` | `URLField` | `blank=True` |
| `fecha_creacion` | `DateTimeField` | `auto_now_add=True` |
| `usuarios` | `ManyToManyField` | `through="Pertenencia"`, `related_name="grupos"` |
| `juegos` | `ManyToManyField` | `blank=True`, `related_name="grupos"` |

La relación con los usuarios utiliza el modelo intermedio `Pertenencia`, que almacena información adicional sobre la pertenencia. La relación con los videojuegos utiliza una tabla intermedia generada automáticamente por Django.

### 4.7. Pertenencia

Representa la pertenencia de un usuario a un grupo y almacena información adicional de esa relación.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `grupo` | `ForeignKey` | `on_delete=CASCADE` |
| `rol` | `CharField` | `max_length=30`, `default="miembro"` |
| `fecha_union` | `DateTimeField` | `auto_now_add=True` |
| `fecha_salida` | `DateTimeField` | `null=True`, `blank=True` |

Es el modelo intermedio de la relación muchos a muchos entre usuarios y grupos.

### 4.8. Juego

Representa los videojuegos registrados en la plataforma.

| Campo | Tipo | Parámetros |
|---|---|---|
| `nombre` | `CharField` | `max_length=100` |
| `descripcion` | `TextField` | `blank=True` |
| `genero` | `CharField` | `max_length=50` |
| `imagen` | `URLField` | `blank=True` |
| `fecha_lanzamiento` | `DateField` | `null=True`, `blank=True` |
| `plataformas` | `CharField` | `max_length=200`, `blank=True` |

### 4.9. Noticia

Almacena noticias sobre videojuegos y la comunidad.

| Campo | Tipo | Parámetros |
|---|---|---|
| `titulo` | `CharField` | `max_length=200` |
| `contenido` | `TextField` | Sin parámetros adicionales declarados |
| `fecha_publicacion` | `DateTimeField` | `auto_now_add=True` |
| `autor` | `ForeignKey` | `on_delete=CASCADE` |
| `grupo` | `ForeignKey` | `on_delete=CASCADE`, `null=True`, `blank=True` |
| `juego` | `ForeignKey` | `on_delete=CASCADE` |

El grupo asociado a una noticia es opcional. Cada noticia tiene un autor y está relacionada con un videojuego.

### 4.10. Comentario

Representa comentarios publicados en noticias.

| Campo | Tipo | Parámetros |
|---|---|---|
| `contenido` | `TextField` | Sin parámetros adicionales declarados |
| `fecha` | `DateTimeField` | `auto_now_add=True` |
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `noticia` | `ForeignKey` | `on_delete=CASCADE`, `related_name="comentarios"` |

### 4.11. Reaccion

Representa la reacción de un usuario ante una noticia.

| Campo | Tipo | Parámetros |
|---|---|---|
| `tipo` | `CharField` | `max_length=20`, `choices=TIPO_CHOICES` |
| `fecha` | `DateTimeField` | `auto_now_add=True` |
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `noticia` | `ForeignKey` | `on_delete=CASCADE` |

Las opciones de `tipo` son:

- `me_gusta`: Me gusta.
- `no_me_gusta`: No me gusta.

### 4.12. UsuarioJuego

Almacena la asociación entre usuarios y videojuegos, junto con datos de su actividad.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `juego` | `ForeignKey` | `on_delete=CASCADE` |
| `horas_jugadas` | `FloatField` | `default=0` |
| `favorito` | `BooleanField` | `default=False` |
| `fecha_inicio` | `DateField` | `null=True`, `blank=True` |

Este modelo dispone de dos claves foráneas y atributos adicionales. No se declara como tabla intermedia de una relación `ManyToManyField` mediante `through`.

### 4.13. Chat

Representa conversaciones privadas o grupales.

| Campo | Tipo | Parámetros |
|---|---|---|
| `tipo` | `CharField` | `max_length=10`, `choices=TIPO_CHOICES` |
| `fecha_creacion` | `DateTimeField` | `auto_now_add=True` |
| `nombre` | `CharField` | `max_length=100`, `blank=True` |
| `participantes` | `ManyToManyField` | `through="ParticipanteChat"`, `related_name="chats"` |

Las opciones de `tipo` son `privado` y `grupal`.

### 4.14. ParticipanteChat

Es el modelo intermedio que relaciona usuarios y chats.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `chat` | `ForeignKey` | `on_delete=CASCADE` |
| `fecha_union` | `DateTimeField` | `auto_now_add=True` |
| `rol` | `CharField` | `max_length=30`, `default="miembro"` |

### 4.15. Mensaje

Almacena mensajes enviados dentro de los chats.

| Campo | Tipo | Parámetros |
|---|---|---|
| `contenido` | `TextField` | Sin parámetros adicionales declarados |
| `fecha_envio` | `DateTimeField` | `auto_now_add=True` |
| `autor` | `ForeignKey` | `on_delete=CASCADE` |
| `chat` | `ForeignKey` | `on_delete=CASCADE` |

### 4.16. Notificacion

Representa las notificaciones dirigidas a los usuarios.

| Campo | Tipo | Parámetros |
|---|---|---|
| `tipo` | `CharField` | `max_length=20`, `choices=TIPO_CHOICES` |
| `mensaje` | `TextField` | Sin parámetros adicionales declarados |
| `fecha` | `DateTimeField` | `auto_now_add=True` |
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `leida` | `BooleanField` | `default=False` |

Las opciones de `tipo` son `amistad`, `comentario`, `mensaje` y `grupo`.

## 5. Relaciones entre modelos

### 5.1. Relaciones uno a uno (OneToOne)

Se utiliza `OneToOneField` para establecer una relación exclusiva entre dos registros.

| Modelo principal | Modelo relacionado | Campo de relación |
|---|---|---|
| `Usuario` | `PerfilUsuario` | `PerfilUsuario.usuario` |
| `Usuario` | `ConfiguracionUsuario` | `ConfiguracionUsuario.usuario` |
| `Usuario` | `EstadisticasUsuario` | `EstadisticasUsuario.usuario` |

Cada perfil, configuración y registro de estadísticas pertenece a un único usuario. Un usuario puede tener como máximo un registro relacionado de cada uno de estos modelos.

### 5.2. Relaciones uno a muchos (ForeignKey)

Se implementan mediante `ForeignKey`. Desde la perspectiva del modelo que contiene la clave foránea, son relaciones muchos a uno.

| Modelo que contiene la clave foránea | Modelo relacionado | Campo |
|---|---|---|
| `Amistad` | `Usuario` | `usuario_origen` |
| `Amistad` | `Usuario` | `usuario_destino` |
| `Pertenencia` | `Usuario` | `usuario` |
| `Pertenencia` | `Grupo` | `grupo` |
| `Noticia` | `Usuario` | `autor` |
| `Noticia` | `Grupo` | `grupo` |
| `Noticia` | `Juego` | `juego` |
| `Comentario` | `Usuario` | `usuario` |
| `Comentario` | `Noticia` | `noticia` |
| `Reaccion` | `Usuario` | `usuario` |
| `Reaccion` | `Noticia` | `noticia` |
| `UsuarioJuego` | `Usuario` | `usuario` |
| `UsuarioJuego` | `Juego` | `juego` |
| `ParticipanteChat` | `Usuario` | `usuario` |
| `ParticipanteChat` | `Chat` | `chat` |
| `Mensaje` | `Usuario` | `autor` |
| `Mensaje` | `Chat` | `chat` |
| `Notificacion` | `Usuario` | `usuario` |

El campo `Noticia.grupo` permite valores nulos, por lo que una noticia puede no estar asociada a ningún grupo.

### 5.3. Relaciones muchos a muchos (ManyToMany)

| Modelo principal | Modelo relacionado | Implementación | Atributos adicionales |
|---|---|---|---|
| `Grupo` | `Usuario` | `ManyToManyField` mediante `Pertenencia` | `rol`, `fecha_union`, `fecha_salida` |
| `Chat` | `Usuario` | `ManyToManyField` mediante `ParticipanteChat` | `fecha_union`, `rol` |
| `Grupo` | `Juego` | `ManyToManyField` con tabla intermedia automática | No declarados |

Los modelos `Pertenencia` y `ParticipanteChat` permiten almacenar datos adicionales de las relaciones.

**Nota sobre UsuarioJuego:** en el código del proyecto, `UsuarioJuego` tiene dos `ForeignKey`, pero no consta un `ManyToManyField` que lo utilice mediante `through`. Por ello, no se contabiliza como una relación muchos a muchos declarada formalmente.

## 6. Tipos de campos utilizados

Los modelos emplean los siguientes tipos de campos de Django:

| Tipo de campo | Descripción |
|---|---|
| `CharField` | Texto de longitud limitada. |
| `TextField` | Texto largo. |
| `BooleanField` | Valor verdadero o falso. |
| `PositiveIntegerField` | Entero no negativo. |
| `PositiveSmallIntegerField` | Entero pequeño no negativo. |
| `FloatField` | Número de coma flotante. |
| `DecimalField` | Número decimal con precisión definida. |
| `DateField` | Fecha. |
| `DateTimeField` | Fecha y hora. |
| `URLField` | Dirección URL. |
| `OneToOneField` | Relación uno a uno. |
| `ForeignKey` | Relación muchos a uno. |
| `ManyToManyField` | Relación muchos a muchos. |

Los tres últimos son campos relacionales; los diez primeros son tipos de campos no relacionales.

## 7. Parámetros de los campos

| Parámetro | Descripción | Ejemplo en el proyecto |
|---|---|---|
| `max_length` | Longitud máxima de un campo de texto. | `max_length=100` |
| `blank` | Permite dejar vacío un campo durante la validación. | `blank=True` |
| `null` | Permite almacenar `NULL` en la base de datos. | `null=True` |
| `default` | Establece un valor predeterminado. | `default=False` |
| `auto_now_add` | Establece automáticamente la fecha y hora al crear el registro. | `auto_now_add=True` |
| `on_delete` | Define el comportamiento al eliminar el objeto relacionado. | `on_delete=CASCADE` |
| `related_name` | Define el nombre de acceso inverso a la relación. | `related_name="comentarios"` |
| `max_digits` | Número máximo de dígitos de un `DecimalField`. | `max_digits=4` |
| `decimal_places` | Número de cifras decimales de un `DecimalField`. | `decimal_places=2` |
| `choices` | Define las opciones disponibles para un campo. | `choices=TIPO_CHOICES` |
| `through` | Especifica el modelo intermedio de una relación muchos a muchos. | `through="Pertenencia"` |

**Diferencia entre `blank` y `null`:** `blank` afecta a la validación del campo; `null` afecta al almacenamiento en la base de datos.

## 8. Diagrama entidad-relación

<img width="1085" height="789" alt="modelo entidad relacion" src="https://github.com/user-attachments/assets/b4fe0312-9f53-4b35-85ca-c85609affbd4" />

<img width="1536" height="1024" alt="modelo relacional" src="https://github.com/user-attachments/assets/e3abb246-dce2-4e7c-b1a7-fe00ea999493" />

## 9. Generación de datos de prueba

El proyecto dispone de un comando personalizado ubicado en:

`core/management/commands/seed.py`

Para ejecutarlo:

```bash
python manage.py seed
```

El comando permite generar datos de prueba para comprobar los modelos y sus relaciones.

Si el requisito de la práctica es crear diez registros aleatorios por cada modelo, debe verificarse que la implementación de `seed.py` genere diez registros de cada modelo y respete las dependencias entre entidades.

## 10. Instalación y ejecución inicial

Los siguientes comandos se ejecutan desde la carpeta raíz del proyecto.

### 10.1. Crear y activar el entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 10.2. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 10.3. Crear y aplicar migraciones

Si todavía no existen migraciones para los modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

Si las migraciones ya existen en el repositorio:

```bash
python manage.py migrate
```

### 10.4. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 10.5. Iniciar el servidor

```bash
python manage.py runserver
```

Por defecto, el servidor de desarrollo estará disponible en:

`http://127.0.0.1:8000/`

## 11. Copias de seguridad

Django permite exportar e importar datos mediante fixtures.

### 11.1. Exportar los datos

Para generar una copia de seguridad en `backup.json`:

```bash
python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission --exclude=sessions --indent 2 -o backup.json
```

### 11.2. Importar los datos

Para cargar los datos del archivo:

```bash
python manage.py loaddata backup.json
```

Antes de restaurar una copia, deben estar aplicadas las migraciones correspondientes. Es recomendable comprobar que el fixture puede importarse correctamente en una base de datos compatible.

## 12. Control de versiones

Git permite registrar los cambios del proyecto y mantener diferentes ramas de trabajo.

Las ramas utilizadas durante esta parte son:

- `Configuracion_inicial`: configuración inicial del proyecto.
- `Modelos`: desarrollo de los modelos y sus relaciones.
- `Backups`: trabajo relacionado con las copias de seguridad.
- `main`: rama principal del proyecto.

El archivo `.gitignore` debe excluir el entorno virtual (`.venv/` o `venv/`), `__pycache__/`, los archivos compilados de Python y las configuraciones locales sensibles.

Deben mantenerse en el repositorio los archivos necesarios para ejecutar y evaluar el proyecto, como `requirements.txt`, las migraciones y los fixtures cuando corresponda.

## 13. Conclusión

GameLoop aplica conceptos de desarrollo web con Django y Python mediante modelos, relaciones entre entidades, datos de prueba y copias de seguridad.

---

# Creación Aplicación Web Parte II

## 14. Objetivo

En esta segunda parte de GameLoop se amplía la aplicación mediante diez funcionalidades, utilizando URLs, vistas, plantillas HTML y consultas QuerySet de Django.

Se trabaja con las relaciones OneToOne, ManyToOne y ManyToMany, así como con filtros, agregaciones y optimización de consultas.

## 15. URLs y vistas implementadas

Se han creado diez funcionalidades principales y una ruta adicional mediante `re_path()`.

| URL | Vista | Funcionalidad |
|---|---|---|
| `/` | `index` | Índice principal. |
| `/usuarios/` | `lista_usuarios` | Listado de usuarios. |
| `/usuarios/<int:usuario_id>/` | `detalle_usuario` | Detalle de usuario y relaciones. |
| `/juegos/` | `lista_juegos` | Listado de videojuegos. |
| `/grupos/` | `lista_grupos` | Listado de grupos. |
| `/grupos/<int:grupo_id>/<str:rol>/` | `detalle_grupo` | Detalle de grupo filtrado por rol. |
| `/noticias/` | `lista_noticias` | Listado de noticias. |
| `/noticias/<int:noticia_id>/` | `detalle_noticia` | Detalle de noticia. |
| `/estadisticas/` | `estadisticas` | Estadísticas generales. |
| `/buscar/<str:termino>/` | `buscar_juego` | Búsqueda de videojuegos. |
| `/buscar-regex/<termino>/` | `buscar_juego` | Búsqueda utilizando `re_path()`. |

Las rutas están definidas en `core/urls.py` y cada una está asociada a su correspondiente vista en `core/views.py`.

## 16. Relaciones entre modelos

Las vistas recuperan información relacionada mediante los diferentes tipos de relaciones:

- **OneToOne:** perfil, configuración y estadísticas de los usuarios.
- **ManyToMany:** usuarios y grupos, juegos y grupos, participantes de chats.
- **ManyToOne:** noticias, autores, comentarios, reacciones, amistades y mensajes.

Para obtener esta información se utilizan `select_related()` y `prefetch_related()`, que permiten optimizar la recuperación de datos relacionados.

## 17. Consultas QuerySet

En las vistas se utilizan diferentes métodos del ORM de Django:

| Método o función | Utilización |
|---|---|
| `all()` | Recupera todos los registros de una consulta. |
| `filter()` | Filtra registros según determinadas condiciones. |
| `exclude()` | Excluye registros que cumplen determinadas condiciones. |
| `order_by()` | Ordena los resultados. |
| `select_related()` | Recupera relaciones ForeignKey y OneToOne mediante JOIN. |
| `prefetch_related()` | Recupera relaciones ManyToMany y relaciones inversas mediante consultas adicionales. |
| `annotate()` | Añade cálculos a los resultados de una consulta. |
| `aggregate()` | Calcula valores generales sobre un conjunto de registros. |
| `exists()` | Comprueba si una consulta devuelve resultados. |
| `Q()` | Permite combinar condiciones de búsqueda. |

También se utilizan `Count()`, `Avg()` y `Sum()` para realizar operaciones de agregación.

### 17.1. Combinación de filtros

Se utilizan condiciones AND y OR mediante filtros y objetos `Q()` para combinar diferentes criterios de búsqueda.

### 17.2. Agregaciones

Se utilizan `annotate()` y `aggregate()` para obtener información calculada a partir de los registros, como recuentos y medias.

### 17.3. Relaciones inversas

Las consultas también acceden a los datos relacionados desde el modelo contrario, utilizando los nombres de relación inversa definidos en los modelos.

### 17.4. Optimización de consultas

Se utilizan:

- `select_related()` para relaciones OneToOne y ForeignKey.
- `prefetch_related()` para relaciones ManyToMany y relaciones inversas.

Estas funciones permiten reducir las consultas innecesarias a la base de datos.

### 17.5. Ordenación y limitación

Se utiliza `order_by()` para ordenar los resultados y cortes de QuerySet para limitar el número de registros devueltos.

### 17.6. Filtrado de valores nulos

En el modelo intermedio `Pertenencia` se utiliza un campo nullable para filtrar las pertenencias que todavía no tienen fecha de salida:

```python
.filter(fecha_salida__isnull=True)
```

### 17.7. Consultas SQL

Se incluyen comentarios en las vistas con la consulta SQL aproximada correspondiente a cada QuerySet.

## 18. Obtención de datos entre tablas relacionadas

Las vistas utilizan las relaciones definidas en los modelos para recuperar información de distintas tablas.

**OneToOne:**

- Se recupera el perfil de cada usuario.
- Se consultan sus preferencias de configuración.
- Se obtienen sus estadísticas personales.

**ManyToMany:**

- Se obtienen los usuarios pertenecientes a cada grupo.
- Se recuperan los juegos asociados a los grupos.
- Se consultan los participantes de los chats.

**ManyToOne:**

- Se recuperan las noticias junto con sus autores y juegos.
- Se consultan los comentarios y las reacciones de cada noticia.
- Se obtienen las amistades enviadas y recibidas por cada usuario.
- Se recuperan los mensajes y las notificaciones de los usuarios.

## 19. Plantillas HTML

Las plantillas se encuentran en:

`core/templates/core/`

Se utiliza `base.html` para mantener una estructura común en las diferentes páginas.

Entre las plantillas principales se encuentran:

| Plantilla | Funcionalidad |
|---|---|
| `index.html` | Índice principal con acceso a las funcionalidades. |
| `usuarios.html` | Muestra el listado de usuarios. |
| `usuario_detalle.html` | Muestra los datos y relaciones de un usuario. |
| `juegos.html` | Muestra los videojuegos. |
| `grupos.html` | Muestra los grupos, usuarios y juegos relacionados. |
| `grupo_detalle.html` | Muestra los miembros de un grupo y sus roles. |
| `noticias.html` | Muestra las noticias publicadas. |
| `noticia_detalle.html` | Muestra una noticia, sus comentarios y reacciones. |
| `estadisticas.html` | Muestra estadísticas de los usuarios. |
| `buscar_juego.html` | Muestra los resultados de búsqueda. |

El índice principal permite acceder a las funcionalidades implementadas.

## 20. Errores personalizados

Se han creado páginas de error personalizadas para los siguientes códigos:

| Código | Descripción | Plantilla |
|---|---|---|
| 400 | Petición incorrecta. | `400.html` |
| 403 | Acceso prohibido. | `403.html` |
| 404 | Página no encontrada. | `404.html` |
| 500 | Error interno del servidor. | `500.html` |

Las plantillas se encuentran en la carpeta de errores dentro de `core/templates/core/`.

Los manejadores se encuentran en `core/views.py` y están registrados en `GameLoop/urls.py`.

## 21. Fixture y datos de prueba

El proyecto incluye un fixture llamado `datos.json`, ubicado en:

`core/fixtures/datos.json`

Este archivo contiene 40 objetos de prueba relacionados entre los distintos modelos de la aplicación.

Entre los datos incluidos se encuentran:

- Usuarios y sus perfiles.
- Configuraciones y estadísticas.
- Videojuegos.
- Grupos y pertenencias.
- Amistades.
- Noticias, comentarios y reacciones.
- Chats, participantes y mensajes.
- Notificaciones.

### 21.1. Cargar los datos de prueba

Para cargar los datos del fixture se utiliza:

```bash
python manage.py loaddata core/fixtures/datos.json
```

### 21.2. Generar nuevamente el fixture

Para exportar los datos de la aplicación:

```bash
python manage.py dumpdata core --indent 4 --output core/fixtures/datos.json
```

Se ha comprobado la carga correcta del archivo mediante Django, obteniendo el resultado de 40 objetos instalados.

## 22. Configuración en modo Producción

Se ha configurado el proyecto para trabajar con los ajustes de producción de Django.

Entre los cambios realizados se encuentran:

- `DEBUG = False` para desactivar el modo de depuración.
- Configuración de `ALLOWED_HOSTS` para establecer los hosts permitidos.
- Uso de una variable de entorno `DJANGO_SECRET_KEY` para la clave secreta.
- Configuración de `STATIC_URL` y `STATIC_ROOT` para gestionar los archivos estáticos.

### 22.1. Comprobación de seguridad

Para comprobar la configuración de seguridad se utiliza:

```bash
python manage.py check --deploy
```

Esta comprobación permite detectar advertencias relacionadas con la seguridad del proyecto.

En el entorno local quedan pendientes algunas medidas relacionadas con HTTPS, que deben configurarse cuando se despliegue la aplicación en un servidor con certificado SSL.

### 22.2. Recopilación de archivos estáticos

Para recopilar los archivos estáticos se utiliza:

```bash
python manage.py collectstatic --noinput
```

## 23. Instalación y ejecución de la Parte II

Los siguientes comandos se ejecutan desde la carpeta raíz del proyecto.

### 23.1. Crear el entorno virtual

```powershell
python -m venv .venv
```

### 23.2. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 23.3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 23.4. Configurar la clave secreta

La variable de entorno `DJANGO_SECRET_KEY` debe estar configurada antes de iniciar el proyecto.

En PowerShell:

```powershell
$env:DJANGO_SECRET_KEY="TU_CLAVE_SECRETA"
```

Debe utilizarse una clave secreta propia y no compartirla públicamente.

### 23.5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 23.6. Cargar el fixture

```bash
python manage.py loaddata core/fixtures/datos.json
```

### 23.7. Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 23.8. Iniciar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en:

`http://127.0.0.1:8000/`

## 24. Control de versiones y ramas

Se utiliza Git y GitHub para gestionar los cambios del proyecto.

Durante la segunda parte se ha trabajado en la rama:

`Aplicación-Web-Parte-2`

Cada funcionalidad se ha desarrollado mediante una rama independiente y posteriormente se ha fusionado con la rama de la tarea.

Finalmente, los cambios se han integrado en la rama principal `main` y se han sincronizado con el repositorio remoto.

El archivo `.gitignore` excluye los entornos virtuales, archivos temporales, caché de Python y configuraciones locales sensibles.

Se mantienen en el repositorio los archivos necesarios para ejecutar y evaluar el proyecto, incluyendo las migraciones, `requirements.txt` y el fixture `datos.json`.

## 25. Conclusión

En esta segunda parte se han implementado diez funcionalidades mediante URLs, vistas, plantillas y consultas QuerySet.

También se han trabajado las relaciones entre modelos, la optimización de consultas, las agregaciones, las páginas de error personalizadas, la creación de datos de prueba mediante fixtures y la configuración de Django en modo Producción.

Con estas mejoras se amplía GameLoop y se ponen en práctica los conocimientos de URLs, Views, plantillas y acceso a bases de datos mediante el ORM de Django.
