#GONZALEZ PACHECO SOFIA CAMILA
import customtkinter as ctk
import config
from estructuras.tabla_hash import TablaHash
from estructuras.arboles import ArbolBST
from backend.persistence_manager import PersistenceManager
from gui.app_window import AppWindow

def main():
    print("Iniciando Sistema OMCA...")

    config.tabla_hash = TablaHash(10)
    config.arbol_inventario = ArbolBST()

    
    config.persistence_manager = PersistenceManager(
        config.RUTA_USUARIOS_CSV, 
        config.RUTA_PRODUCTOS_CSV
    )

    try:
        config.persistence_manager.cargarUsuarios(config.tabla_hash)
        print("✓ Usuarios cargados en Tabla Hash.")
    except FileNotFoundError:
        print(" No se encontró usuarios.csv, iniciando con Tabla Hash vacía.")

    try:
        config.persistence_manager.cargarProductos(config.arbol_inventario)
        print("✓ Inventario cargado en Árbol BST.")
    except FileNotFoundError:
        print(" No se encontró productos.csv, iniciando con Árbol vacío.")

    # 6. Configurar la Interfaz Visual (CustomTkinter)
    ctk.set_appearance_mode("dark")        # Modos: "dark", "light", "system"
    ctk.set_default_color_theme("blue")    # Temas: "blue", "green", "dark-blue"
    
    app = AppWindow() # Esta será tu clase principal que hereda de ctk.CTk

    # 8. Arrancar el ciclo de eventos visuales
    print("Desplegando Interfaz Gráfica (Menú Principal)...")
    app.mainloop()

    
if __name__ == "__main__":
    main()