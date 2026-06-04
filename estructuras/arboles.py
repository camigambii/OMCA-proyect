class Producto:


    COLORIMETRIAS = {
        1: "calido",
        2: "frio",
        3: "universal"
    }

    GAMAS = {
        1: "barato",
        2: "intermedio",
        3: "caro"
    }

    TIPOS_PRODUCTO = {
        1: "bronzer",
        2: "gloss",
        3: "paleta",
        4: "rubor",
        5: "producto universal"
    }

    CATEGORIAS_VALIDAS = [
        "accesorios",
        "bronzer",
        "gloss",
        "paleta",
        "rubor",
        "producto universal"
    ]


    def __init__(
        self,
        id,
        nombre,
        categoria,
        precio,
        stock,
        ruta_imagen,
        color_r,
        color_g,
        color_b
    ):


        self.validar_id(id)

        self.validar_precio(precio)

        self.validar_stock(stock)

        self.validar_categoria(categoria)

        self.validar_rgb(
            color_r,
            color_g,
            color_b
        )


        self.id = id

        self.nombre = nombre

        self.categoria = categoria.lower()

        self.precio = float(precio)

        self.stock = int(stock)

        self.ruta_imagen = ruta_imagen

        self.color_r = int(color_r)

        self.color_g = int(color_g)

        self.color_b = int(color_b)

    @staticmethod
    def validar_id(id_producto):
        """
        Valida la estructura:

        [C][G][T][NN]

        Ejemplo:
            31501
        """

        id_str = str(id_producto)

        # Debe contener solo números
        if not id_str.isdigit():

            raise ValueError(
                "El ID debe contener solo números"
            )

        # Debe tener exactamente 5 dígitos
        if len(id_str) != 5:

            raise ValueError(
                "El ID debe tener exactamente 5 dígitos"
            )


        colorimetria = int(id_str[0])

        gama = int(id_str[1])

        tipo = int(id_str[2])


        if colorimetria not in [1, 2, 3]:

            raise ValueError(
                "Código de colorimetría inválido "
                "(1=cálido, 2=frío, 3=universal)"
            )


        if gama not in [1, 2, 3]:

            raise ValueError(
                "Código de gama inválido "
                "(1=barato, 2=intermedio, 3=caro)"
            )


        if tipo not in [1, 2, 3, 4, 5]:

            raise ValueError(
                "Código de tipo inválido "
                "(1=bronzer, 2=gloss, "
                "3=paleta, 4=rubor, "
                "5=producto universal)"
            )


    @staticmethod
    def validar_precio(precio):

        if precio < 0:

            raise ValueError(
                "El precio no puede ser negativo"
            )


    @staticmethod
    def validar_stock(stock):

        if stock < 0:

            raise ValueError(
                "El stock no puede ser negativo"
            )


    def validar_categoria(self, categoria):

        if categoria.lower() not in self.CATEGORIAS_VALIDAS:

            raise ValueError(
                "Categoría inválida"
            )


    @staticmethod
    def validar_rgb(r, g, b):

        colores = [r, g, b]

        for valor in colores:

            if not isinstance(valor, int):

                raise ValueError(
                    "RGB debe ser entero"
                )

            if valor < 0 or valor > 255:

                raise ValueError(
                    "RGB debe estar entre 0 y 255"
                )

    def obtener_colorimetria(self):
        """
        Retorna:
        calido, frio o universal
        """

        codigo = int(str(self.id)[0])

        return self.COLORIMETRIAS[codigo]

    def obtener_gama(self):
        """
        Retorna:
        barato, intermedio o caro
        """

        codigo = int(str(self.id)[1])

        return self.GAMAS[codigo]

    def obtener_tipo_producto(self):
        """
        Retorna el tipo interno.
        """

        codigo = int(str(self.id)[2])

        return self.TIPOS_PRODUCTO[codigo]

    def obtener_consecutivo(self):
        """
        Retorna:
        01, 02, 03...
        """

        return str(self.id)[3:5]


    def obtener_rgb(self):

        return (
            self.color_b,
            self.color_g,
            self.color_r
        )


    def __str__(self):

        return (
            f"ID: {self.id} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock} | "
            f"Colorimetría: {self.obtener_colorimetria()} | "
            f"Gama: {self.obtener_gama()} | "
            f"Tipo: {self.obtener_tipo_producto()} | "
            f"RGB: ({self.color_r}, "
            f"{self.color_g}, "
            f"{self.color_b})"
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
