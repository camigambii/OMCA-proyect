def busqueda_lineal(lista, texto_buscado, campo="nombre"):

    resultados = []

    texto_buscado = texto_buscado.lower()

    for producto in lista:

        valor_campo = str(
            getattr(producto, campo)
        ).lower()

        if texto_buscado in valor_campo:
            resultados.append(producto)

    return resultados


def busqueda_binaria(
    lista_ordenada,
    valor_buscado,
    campo="id"
):

    bajo = 0
    alto = len(lista_ordenada) - 1

    while bajo <= alto:

        medio = (bajo + alto) // 2

        producto_medio = lista_ordenada[medio]

        valor_medio = getattr(
            producto_medio,
            campo
        )

        # Encontrado
        if valor_medio == valor_buscado:
            return producto_medio

        # Buscar izquierda
        elif valor_buscado < valor_medio:
            alto = medio - 1

        # Buscar derecha
        else:
            bajo = medio + 1

    # No encontrado
    return None
