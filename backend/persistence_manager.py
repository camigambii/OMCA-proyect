#GONZAlez pacheco sfoai camila
import csv
from estructuras.tabla_hash import Usuario
from estructuras.arboles import Producto
class PersistenceManager:
    def __init__(self,rutaUsuarios,rutaProductos):
        self.rutaUsuarios=rutaUsuarios
        self.rutaProductos=rutaProductos



    def cargarUsuarios(self,tabla_hash):
        with open(self.rutaUsuarios,mode='r', newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                username=fila["username"]
                password=fila["password"]
                rol=fila["rol"]
                nuevo_usuario=Usuario(username,password,rol)
                tabla_hash.insertar(nuevo_usuario)



    def guardarUsuarios(self,tabla_hash):
        lista_usuarios = tabla_hash.obtener_todos()
        with open(self.rutaUsuarios, mode='w',newline='', encoding='utf-8') as archivo:
            nombres_columnas = ["username", "password", "rol"]
            escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
            escritor.writeheader()
        
            for usuario in lista_usuarios:
                escritor.writerow({
                    "username": usuario.username,
                    "password": usuario.password,
                    "rol": usuario.rol
                })


#CONSIDERA QUE YA SE ORGANIZO COMO BGR DESDE AQUI
    def cargarProductos(self,arbol):
        with open(self.rutaProductos, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                id=int(fila["id"])
                nombre=fila["nombre"]
                categoria=fila["categoria"]
                precio=float(fila["precio"])
                stock=int(fila["stock"])
                ruta_imagen=fila["ruta_imagen"]
                color_r=int(fila["color_r"])
                color_g=int(fila["color_g"])
                color_b=int(fila["color_b"])
                    
                nuevo_producto = Producto(id, nombre, categoria, precio, stock, ruta_imagen,color_b, color_g, color_r)
                arbol.insertar(nuevo_producto)

def guardarProductos(self,arbol):
    lista_productos = arbol.obtener_lista_inorden()
    with open(self.rutaProductos, mode='w', newline='', encoding='utf-8') as archivo:
            
            
            nombres_columnas = ["id", "nombre", "categoria", "precio", "stock", "ruta_imagen", "color_r", "color_g", "color_b"]
            
            escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
            escritor.writeheader()
            
            
            for producto in lista_productos:
                escritor.writerow({
                    "id": producto.id,
                    "nombre": producto.nombre,
                    "categoria": producto.categoria,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "ruta_imagen": producto.ruta_imagen,
                    # NOTA: Asegúrate de que los nombres de los atributos (.color_r, etc.) 
                    # coincidan exactamente con cómo los guardaste dentro de tu clase Producto
                    "color_r": producto.color_r,
                    "color_g": producto.color_g,
                    "color_b": producto.color_b
                })
                