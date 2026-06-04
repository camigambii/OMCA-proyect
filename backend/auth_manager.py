from estructuras.tabla_hash import Usuario

import config


def login(username, password):
    """
    Verifica credenciales de acceso.

    Retorna:
    - "admin"
    - "cliente"
    - None
    """

    # Buscar usuario en la tabla hash
    usuario = config.tabla_hash.buscar(username)

    # Usuario no existe
    if usuario is None:
        return None

    # Contraseña incorrecta
    if usuario.password != password:
        return None

    # Guardar usuario activo
    config.USUARIO_ACTIVO = usuario

    # Retornar rol
    return usuario.rol


def registrar(username, password):
    """
    Registra un nuevo usuario cliente.

    Retorna:
    - True si se registró correctamente
    - False si el usuario ya existe
    """

    # Verificar si ya existe
    usuario_existente = config.tabla_hash.buscar(
        username
    )

    if usuario_existente is not None:
        return False

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        username,
        password,
        "cliente"
    )

    # Insertar en tabla hash
    config.tabla_hash.insertar(
        nuevo_usuario
    )

    # Guardar inmediatamente en CSV
    config.persistence_manager.guardar_usuarios(
        config.tabla_hash
    )

    return True


def eliminar_usuario(username):
    """
    Elimina un usuario del sistema.

    Retorna:
    - True si se eliminó
    - False si no existía
    """

    resultado = config.tabla_hash.eliminar(
        username
    )

    # Actualizar CSV
    if resultado:

        config.persistence_manager.guardar_usuarios(
            config.tabla_hash
        )

    return resultado

def cerrar_sesion():
    """
    Cierra la sesión actual.
    """

    config.USUARIO_ACTIVO = None