class Producto:

    def __init__(self, id, nombre, categoria, precio, stock, ruta_imagen):
        categorias_validas = ["Labiales", "Rubores", "Sombras", "Bronzers"]

        if categoria not in categorias_validas:
            raise ValueError(
                f"La categoría debe ser una de: {categorias_validas}"
            )

        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.ruta_imagen = ruta_imagen

    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock}"
        )


class NodoArbol:

    def __init__(self, producto):
        self.producto = producto
        self.izquierdo = None
        self.derecho = None


class ArbolBST:

    def __init__(self):
        self.raiz = None


    def insertar(self, producto):

        nuevo_nodo = NodoArbol(producto)

        # Árbol vacío
        if self.raiz is None:
            self.raiz = nuevo_nodo
            return

        self._insertar_recursivo(self.raiz, nuevo_nodo)

    def _insertar_recursivo(self, nodo_actual, nuevo_nodo):

        id_nuevo = nuevo_nodo.producto.id
        id_actual = nodo_actual.producto.id

        # Evitar IDs duplicados
        if id_nuevo == id_actual:
            raise ValueError(
                f"Ya existe un producto con ID {id_nuevo}"
            )

        # Va a la izquierda
        if id_nuevo < id_actual:

            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = nuevo_nodo
            else:
                self._insertar_recursivo(
                    nodo_actual.izquierdo,
                    nuevo_nodo
                )

        # Va a la derecha
        else:

            if nodo_actual.derecho is None:
                nodo_actual.derecho = nuevo_nodo
            else:
                self._insertar_recursivo(
                    nodo_actual.derecho,
                    nuevo_nodo
                )


    def buscar(self, id_producto):

        return self._buscar_recursivo(self.raiz, id_producto)

    def _buscar_recursivo(self, nodo_actual, id_producto):

        # No encontrado
        if nodo_actual is None:
            return None

        id_actual = nodo_actual.producto.id

        # Encontrado
        if id_producto == id_actual:
            return nodo_actual

        # Buscar izquierda
        if id_producto < id_actual:
            return self._buscar_recursivo(
                nodo_actual.izquierdo,
                id_producto
            )

        # Buscar derecha
        return self._buscar_recursivo(
            nodo_actual.derecho,
            id_producto
        )


    def eliminar(self, id_producto):
        """
        Elimina un producto del árbol.
        """

        self.raiz = self._eliminar_recursivo(
            self.raiz,
            id_producto
        )

    def _eliminar_recursivo(self, nodo_actual, id_producto):

        if nodo_actual is None:
            return None

        id_actual = nodo_actual.producto.id

        # Buscar izquierda
        if id_producto < id_actual:

            nodo_actual.izquierdo = self._eliminar_recursivo(
                nodo_actual.izquierdo,
                id_producto
            )

        # Buscar derecha
        elif id_producto > id_actual:

            nodo_actual.derecho = self._eliminar_recursivo(
                nodo_actual.derecho,
                id_producto
            )

        # Nodo encontrado
        else:

            if nodo_actual.izquierdo is None and nodo_actual.derecho is None:
                return None


            # Solo hijo derecho
            if nodo_actual.izquierdo is None:
                return nodo_actual.derecho

            # Solo hijo izquierdo
            if nodo_actual.derecho is None:
                return nodo_actual.izquierdo

            # Buscar sucesor en inorden
            sucesor = self._obtener_minimo(
                nodo_actual.derecho
            )

            # Copiar producto del sucesor
            nodo_actual.producto = sucesor.producto

            # Eliminar sucesor
            nodo_actual.derecho = self._eliminar_recursivo(
                nodo_actual.derecho,
                sucesor.producto.id
            )

        return nodo_actual

    def _obtener_minimo(self, nodo):

        actual = nodo

        while actual.izquierdo is not None:
            actual = actual.izquierdo

        return actual

    def obtener_lista_inorden(self):

        productos = []

        self._inorden_recursivo(self.raiz, productos)

        return productos

    def _inorden_recursivo(self, nodo_actual, lista):

        if nodo_actual is not None:

            # Izquierda
            self._inorden_recursivo(
                nodo_actual.izquierdo,
                lista
            )

            # Nodo actual
            lista.append(nodo_actual.producto)

            # Derecha
            self._inorden_recursivo(
                nodo_actual.derecho,
                lista
            )


    def mostrar_inorden(self):

        productos = self.obtener_lista_inorden()

        if not productos:
            print("El inventario está vacío.")
            return

        for producto in productos:
            print(producto)