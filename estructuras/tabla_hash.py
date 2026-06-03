#GONZAlez pacheco sfoai camila
class Usuario:
    def __init__(self, username, password, rol):
        self.username = username
        self.password = password
        self.rol = rol
        self.carrito = []

class TablaHash:
    def __init__(self, size=None):
        self.size = size
        self.tabla = {} 

    
    def insertar(self, usuario):
        if usuario.username in self.tabla:
            return False
        else:
            self.tabla[usuario.username] = usuario
            return True

    def buscar(self, username):
        if username in self.tabla:
            return self.tabla[username]
        else:
            return None
        
    def eliminar(self, username):
        if username in self.tabla:
            self.tabla.pop(username)
            return True
        else:
            return False

    
    def obtener_todos(self):
        X = list(self.tabla.values())
        return X
    