# Librerías:

- https://django-role-permissions.readthedocs.io/en/stable/quickstart.html
- https://github.com/jazzband/django-tinymce
- https://django-avatar.readthedocs.io/en/latest/#
-

# TODO:
- Generar eventos de mensajes con intentos de login fallidos y bloquear la cuenta.
- BUG: Necesito comentar la clase foro.apiviews.ListPublicationsWithLastComments para poder ejecutar las migraciones.
- PAGINACION EN LOS COMENTARIOS
- Ordenar comentarios y respuestas.
- La vista de perfil en móviles se ve mal.
- Cerrar sesión
- Slug en titles
- Terminar Paginación
- Avisar de que la restauración de la clave se ha hecho con éxito antes de redirigir a login.
- Poner aceptar las cookies, también en los sabías que.
- Arreglar la discrepancia entre estados del avatar y del perfil cuando se cambia la imagen.
- DOCUMENTAR TODO EL CODIGO. En el libro de APIs con django recomiendan frameworks.
- Solucionar problema con los correos: ¿Plantilla html completa?
- Unificar criterio-etiqueta para los artículos: No títulos en mayúsculas.
- Poder subir videos en el editor CKEditor
- Quitar el enlace a foros redundante en el menú para móviles
- Iconos en el navbar para moviles.
- Selenium tests
- GOOGLE ANALYTICS: afinar eventos
- Retardo de una hora entre registro y comentar.
- PropTypes
- /recover_password [Frontend]
- @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
- Encuestas y eventos.
- Migas de pan: https://stackoverflow.com/questions/29244731/react-router-how-to-manually-invoke-link

# Anotaciones:

- /manage.py loaddata users temasblog articlesblog commentsblog temasforo publicacionesforo comentariospublicaciones
- rsync -arv /home/roberto/devel/javascript/comunidad_lsa_frontend/build/\* ovh1:/var/www/comunidad_lsa/
- https://github.com/grantmcconnaughey/django-avatar/blob/master/avatar/models.py
- https://djangotricks.blogspot.com/2020/03/how-to-upload-a-file-using-django-rest-framework.html
- Usar grunt para los tests? https://stackoverflow.com/questions/15166532/how-to-automatically-run-tests-when-theres-any-change-in-my-project-django
- celery -A csa worker -l INFO

# Hechos
- Correos asincronos
- Incrementar contador de lecturas.
- Terminos y condiciones [Frontend]
- Ratelimit: comentarios...
- Quitar recuperar clave hasta que esté implementado
- django.db.utils.DataError: (1406, "Data too long for column 'frase_inspiradora' at row 1") [Solo en el frontend]
- GOOGLE ANALYTICS
- Revisar más campos Meta - Cambiar la descripción e imagen para las redes sociales
- Footer
- Poner firma en footer de artículos.
- Poner avatar en titles de posts. En móvil se ve enano.
- Texto de las noticias es demasiado grande para móviles
- Firma en articleDetail
- ACTIVAR EL ENVIO DE CORREO EN PRO
- Cambiar la contraseña.
- Modificar perfil
- Crear Post
- Enlaces a title en movil y tablets
- vista del perfil
- nabvar en moviles
- favicon
- Vista para los artículos principales
- Modificar comentario
- Generar tokens automáticamente: https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
- Setear la clave con put desde rest no funciona
- El complemento "foro" debe estar incrustado hermano a de blog para que la aplicación no recargue toda la página.
- Dominio?

# Chunks

```
# def post(self, request, format=None):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         new_user = serializer.save()
    #         Token.objects.create(user=new_user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```
