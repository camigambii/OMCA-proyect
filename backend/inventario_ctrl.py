#GONZAlez pacheco sfoai camila

import config
from estructuras.arboles import Producto

def agregar_producto(id, nombre, categoria, precio, stock, ruta_imagen):
    nodoExistente=config.arbol_inventario.buscar(id)
    if nodoExistente is not None:
        return False
    nuevoProducto=Producto(id, nombre, categoria, precio, stock, ruta_imagen)
    config.arbol_inventario._insertar_recursivo(nuevoProducto)
    config.persistence_manager.guardarProductos(config.arbol_inventario)
    return True

def agregarStock(id,cantidad):
    nodoExistente=config.arbol_inventario.buscar(id)
    if nodoExistente is None:
        return False
    nodoExistente.producto.stock+=cantidad
    config.persistence_manager.guardarProductos(config.arbol_inventario)
    return True

def borrarProducto(id):
    nodoExistente=config.arbol_inventario.buscar(id)
    if nodoExistente is None:
        return False
    nodoBorrado=config.arbol_inventario.eliminar(id)
    if nodoExistente:
        config.persistence_manager.guardarProductos(config.arbol_inventario)
    return nodoExistente

def borrarStock(id,cantidad):
    nodoExistente=config.arbol_inventario.buscar(id)
    if nodoExistente is None:
        return False
    
    if nodoExistente.producto.stock>=cantidad:
        nodoExistente.producto.stock-=cantidad
        config.persistence_manager.guardarProductos(config.arbol_inventario)
        return True
    else:
        return False
    
def obtenerTodosProductos():
    return config.arbol_inventario.obtener_lista_inorden()
