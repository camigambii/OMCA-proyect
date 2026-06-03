
def obtener_valor(producto, clave):

    if clave == "precio":
        return producto.precio

    elif clave == "nombre":
        return producto.nombre.lower()

    elif clave == "id":
        return producto.id

    elif clave == "categoria":
        return producto.categoria.lower()

    elif clave == "colorimetria":
        return producto.obtener_colorimetria()

    elif clave == "gama":
        return producto.obtener_gama()

    elif clave == "tipo":
        return producto.obtener_tipo_producto()

    elif clave == "color_r":
        return producto.color_r

    elif clave == "color_g":
        return producto.color_g

    elif clave == "color_b":
        return producto.color_b

    else:

        raise ValueError(
            "Clave inválida"
        )


def quicksort(lista, bajo, alto, clave="precio"):

    if bajo < alto:

        indice_pivote = particion(
            lista,
            bajo,
            alto,
            clave
        )

        # Subarreglo izquierdo
        quicksort(
            lista,
            bajo,
            indice_pivote - 1,
            clave
        )

        # Subarreglo derecho
        quicksort(
            lista,
            indice_pivote + 1,
            alto,
            clave
        )

    return lista


def particion(lista, bajo, alto, clave):
 

    pivote = obtener_valor(lista[alto], clave)

    i = bajo - 1

    for j in range(bajo, alto):

        valor_actual = obtener_valor(
            lista[j],
            clave
        )

        if valor_actual <= pivote:

            i += 1

            # Intercambio
            lista[i], lista[j] = lista[j], lista[i]

    # Colocar pivote en posición final
    lista[i + 1], lista[alto] = (
        lista[alto],
        lista[i + 1]
    )

    return i + 1


def radix_sort(lista):
    """
    Ordena productos por ID usando Radix Sort.
    """

    if len(lista) == 0:
        return lista

    # Encontrar ID máximo
    maximo = max(producto.id for producto in lista)

    exp = 1

    # Pasadas por unidades, decenas, centenas...
    while maximo // exp > 0:

        counting_sort_por_digito(lista, exp)

        exp *= 10

    return lista


def counting_sort_por_digito(lista, exp):

    n = len(lista)

    salida = [None] * n

    conteo = [0] * 10

    # Contar ocurrencias
    for producto in lista:

        indice = (producto.id // exp) % 10

        conteo[indice] += 1

    # Acumulativo
    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    # Construir salida (de derecha a izquierda
    # para mantener estabilidad)
    for i in range(n - 1, -1, -1):

        producto = lista[i]

        indice = (producto.id // exp) % 10

        salida[conteo[indice] - 1] = producto

        conteo[indice] -= 1

    # Copiar a lista original
    for i in range(n):
        lista[i] = salida[i]


def mergesort(lista, clave="nombre"):

    # Caso base
    if len(lista) <= 1:
        return lista

    mitad = len(lista) // 2

    izquierda = lista[:mitad]
    derecha = lista[mitad:]

    # División recursiva
    izquierda_ordenada = mergesort(
        izquierda,
        clave
    )

    derecha_ordenada = mergesort(
        derecha,
        clave
    )

    # Combinar
    return merge(
        izquierda_ordenada,
        derecha_ordenada,
        clave
    )


def merge(izquierda, derecha, clave):

    resultado = []

    i = 0
    j = 0

    while i < len(izquierda) and j < len(derecha):

        valor_izquierda = obtener_valor(
            izquierda[i],
            clave
        )

        valor_derecha = obtener_valor(
            derecha[j],
            clave
        )

        if valor_izquierda <= valor_derecha:

            resultado.append(izquierda[i])

            i += 1

        else:

            resultado.append(derecha[j])

            j += 1

    # Agregar sobrantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado

def bubblesort(lista, clave="categoria"):

    n = len(lista)

    for i in range(n):

        intercambio = False

        for j in range(0, n - i - 1):

            actual = obtener_valor(
                lista[j],
                clave
            )

            siguiente = obtener_valor(
                lista[j + 1],
                clave
            )

            # Intercambio
            if actual > siguiente:

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

                intercambio = True

        # Si no hubo intercambios,
        # la lista ya está ordenada
        if not intercambio:
            break

    return lista
