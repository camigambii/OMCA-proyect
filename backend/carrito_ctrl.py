#GONZALEZ PACHECO SOFIA CAMILA
from backend import inventario_ctrl
import config



def agregar_al_carrito(producto):
    if producto.stock>0:
        config.USUARIO_ACTIVO.carrito
        return True
    else:
        return False,"producto no disponible"
    
def quitar_del_carrito(idProducto):
    for producto in config.USUARIO_ACTIVO.carrito:
        if producto.id==idProducto:
            config.USUARIO_ACTIVO.carrito.remove(producto)
            break



def obtener_carrito():
    return config.USUARIO_ACTIVO.carrito

def calcular_total():
    cuentaTotal=0
    for producto in config.USUARIO_ACTIVO.carrito:
        cuentaTotal+=producto.precio
    return round(cuentaTotal,2)




def confirmarCompra():
    for producto in config.USUARIO_ACTIVO.carrito:
        inventario_ctrl.borrar_stock(producto.id, 1)
    config.USUARIO_ACTIVO.carrito=[]
    return True




def vaciarCarrito():
    config.USUARIO_ACTIVO.carrito=[]