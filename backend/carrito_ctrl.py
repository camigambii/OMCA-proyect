#GONZALEZ PACHECO SOFIA CAMILA

"""backend/carrito_ctrl.py
Maneja la sesión de compra del cliente que está activo en este momento.
Función agregar_al_carrito(producto):
Accede a config.USUARIO_ACTIVO.carrito
Verifica que el producto tenga stock > 0
Si no tiene stock: retorna False con mensaje "Producto sin stock disponible"
Si tiene stock: agrega el objeto Producto a la lista del carrito
Retorna True
Función quitar_del_carrito(id_producto):
Recorre config.USUARIO_ACTIVO.carrito
Encuentra el producto con ese ID y lo elimina de la lista
Si no lo encuentra: no hace nada
Función obtener_carrito():
Retorna directamente config.USUARIO_ACTIVO.carrito
La GUI lo usa para mostrar el contenido del panel lateral del carrito
Función calcular_total():
Recorre el carrito con un ciclo
Suma todos los producto.precio
Retorna el total como float redondeado a dos decimales
Función confirmar_compra():
Por cada producto en el carrito llama a inventario_ctrl.borrar_stock(producto.id, 1) para descontar una unidad del inventario
Vacía el carrito: config.USUARIO_ACTIVO.carrito = []
Retorna True para que la GUI muestre la pantalla de Orden Confirmada
Función vaciar_carrito():
Pone config.USUARIO_ACTIVO.carrito = []
No guarda nada en CSV porque el carrito no se persiste entre sesiones
"""