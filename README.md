# Ev3-backend
#Nombre de la organizacion: MamboStore  
#Modelo de negocio: Tienda de videojuegos  
#Integrantes: Rodrigo Ide  
#Entidad de Contexto / Agrupación (ORM): Genero de videojuegos  
#Entidad Principal Gestionable (ORM): Videojuegos  
#Propósito de la Sesión (request.session): Carrito de compras con los videojuegos seleccionados y calculo total de la compra    

## Bitacora de prompts  

#Caso 1: Corrección de error de atributo y filtrado en el Carrito de Compras  

#Prompt:  
#"Django me está arrojando `AttributeError` al intentar consultar los ítems del carrito usando `_set` y un `FieldError` con el campo `precio_unitario` en el modelo `ItemPedido`"   

#Repuesta tecnica:   
#La IA identificó que se estaba intentando acceder de forma inversa a una relación que requería el uso del ORM de Django a través del método `.filter()` sobre la relación ForeignKey, y que el modelo `ItemPedido` no poseía el atributo de precio unitario explícito, por lo que la consulta debía realizarse directamente sobre los campos existentes (`pedido` y `videojuego`).  

#Adaptacion aplicada  
#Se reestructuraron las consultas en `apps/carrito/views.py` reemplazando los accesos directos por `ItemPedido.objects.filter(pedido=pedido_activo)` y se ajustó la lógica del cálculo del subtotal utilizando directamente el precio base del modelo `Videojuego` (`item.videojuego.precio * item.cantidad`).  


#Caso 2: Filtrado dinámico del catálogo por parámetros URL (GET)    

#Prompt  
#El filtro por género en el catálogo no está funcionando. Aunque paso `?genero=1` en la URL, la vista sigue retornando todos los videojuegos. ¿Cómo puedo asegurar que la vista lea el parámetro y filtre correctamente?  

#Respuesta tecnica    
#Se sugirió validar la presencia del parámetro `request.GET.get('genero')`, verificar si el valor es numérico (`.isdigit()`) para prevenir fallos de conversión de tipo, y aplicar la consulta con la sintaxis exacta de búsqueda de llave primaria `genero__id=int(genero_id)`.   

#Adaptacion aplicada  
  Se actualizó `catalogo_view` en `apps/juegos/views.py` incluyendo un bloque condicional que convierte de forma segura el `genero_id` recibido por parámetro GET y aplica `Videojuego.objects.filter(genero__id=int(genero_id))`. Además, se pasó la variable `genero_seleccionado` al contexto para resaltar dinámicamente el botón activo en la plantilla HTML.  


#Caso 3: Depuración de enrutamiento y duplicidad de funciones en Vistas  

#Prompt:  
#Agregué la lógica para filtrar por `?genero=1` en `catalogo_view` de Django, pero la página sigue mostrando todos los videojuegos sin aplicar el filtro y los `print` de depuración no se muestran en la consola del servidor.  

#Respuesta Técnica:  
#Se sugirió aplicar una prueba de excepción forzada (`raise Exception`) al inicio de la función para verificar si Django realmente estaba ejecutando el código editado. Al no interrumpirse la ejecución, se identificó que existían dos declaraciones de la función `catalogo_view` dentro del mismo archivo `views.py` (o una sobreescritura de nombres), provocando que Python ejecutara una versión anterior que ignoraba los parámetros GET de la URL.  

#Adaptación Aplicada:  
#Se inspeccionó `apps/juegos/views.py`, se eliminó la definición duplicada de `catalogo_view` y se unificó la lógica en una sola función bien estructurada. Con ello, Django comenzó a interpretar correctamente el parámetro `genero` de la URL y a aplicar la consulta `Videojuego.objects.filter(genero__id=...)`.  