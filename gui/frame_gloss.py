# gui/frames/frame_gloss.py
import customtkinter as ctk
from PIL import Image
import os

# ── Descomentar cuando tengas el backend listo ───────────────────────
"""import config
from backend.inventario_ctrl import obtener_todos_los_productos
from backend.carrito_ctrl    import agregar_al_carrito, calcular_total, confirmar_compra
from estructuras.ordenamiento import quicksort, mergesort
from estructuras.busqueda     import busqueda_lineal"""


# ── Datos de prueba mientras no está el backend ──────────────────────
PRODUCTOS_PRUEBA = [
    {"id": 101, "nombre": "Labial Rojo Mate",   "categoria": "Labiales", "precio": 250.0, "stock": 10, "ruta_imagen": "assets/productos/lab_rojo_mate.png",  "color_bgr": "30-20-180"},
    {"id": 102, "nombre": "Labial Rosa Nude",   "categoria": "Labiales", "precio": 220.0, "stock": 12, "ruta_imagen": "assets/productos/lab_rosa_nude.png",  "color_bgr": "180-150-200"},
    {"id": 103, "nombre": "Labial Coral",        "categoria": "Labiales", "precio": 240.0, "stock": 9,  "ruta_imagen": "assets/productos/lab_coral.png",      "color_bgr": "80-127-255"},
    {"id": 104, "nombre": "Labial Berry",        "categoria": "Labiales", "precio": 260.0, "stock": 11, "ruta_imagen": "assets/productos/lab_berry.png",      "color_bgr": "100-20-140"},
    {"id": 105, "nombre": "Labial Frambuesa",   "categoria": "Labiales", "precio": 245.0, "stock": 8,  "ruta_imagen": "assets/productos/lab_frambuesa.png",  "color_bgr": "60-20-100"},
    {"id": 106, "nombre": "Labial Vino",        "categoria": "Labiales", "precio": 255.0, "stock": 7,  "ruta_imagen": "assets/productos/lab_vino.png",       "color_bgr": "40-10-90"},
]

PLACEHOLDER_COLOR = "#F0ECE8"   # color de fondo cuando no hay imagen
COLS               = 3          # columnas del grid


class FrameGloss(ctk.CTkFrame):
    """
    Catálogo de productos de tipo Labiales / Gloss.
    Incluye: búsqueda, ordenamiento, carrito lateral y botón probar.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#FAFAFA", corner_radius=0)
        self.app       = app
        self.ruta_base = os.path.dirname(
            os.path.dirname(__file__)
        )
        

        # Lista de trabajo (se reemplaza con backend real)
        self._todos    = list(PRODUCTOS_PRUEBA)
        self._visibles = list(self._todos)

        # Carrito local {id: dict_producto}
        self._carrito: list = []

        # Referencias a imágenes (evita garbage collection)
        self._img_refs: dict = {}

        self._construir()
        self._poblar_catalogo(self._visibles)

    # ════════════════════════════════════════════════════════════════════
    # CONSTRUCCIÓN DE LA UI
    # ════════════════════════════════════════════════════════════════════
    def _construir(self):

        # ── Título de sección ────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="G L O S S  &  L A B I A L E S",
            font=("Georgia", 20, "bold"),
            text_color="#1A1A1A"
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            self,
            text="Descubre el tono perfecto para ti",
            font=("Arimo", 12),
            text_color="#888888"
        ).pack(pady=(0, 14))

        # ── Barra de controles ───────────────────────────────────────────
        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(fill="x", padx=30, pady=(0, 12))

        # Buscador
        self.entry_buscar = ctk.CTkEntry(
            barra,
            placeholder_text="🔍  Buscar producto...",
            font=("Arimo", 13),
            width=240,
            height=36,
            corner_radius=18,
            border_color="#DDDDDD",
            fg_color="#FFFFFF"
        )
        self.entry_buscar.pack(side="left", padx=(0, 12))
        self.entry_buscar.bind("<KeyRelease>", self._on_buscar)

        # Ordenamiento
        ctk.CTkLabel(barra, text="Ordenar:", font=("Arimo", 12),
                     text_color="#666666").pack(side="left", padx=(0, 6))

        self.opt_orden = ctk.CTkOptionMenu(
            barra,
            values=["Precio ↑", "Precio ↓", "A → Z", "Z → A"],
            font=("Arimo", 12),
            width=130,
            height=36,
            fg_color="#FFFFFF",
            text_color="#333333",
            button_color="#E8E8E8",
            button_hover_color="#D0D0D0",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#333333",
            command=self._on_ordenar
        )
        self.opt_orden.pack(side="left")

        # ── Cuerpo: catálogo + carrito ───────────────────────────────────
        cuerpo = ctk.CTkFrame(self, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Panel izquierdo — catálogo
        self.panel_catalogo = ctk.CTkScrollableFrame(
            cuerpo,
            fg_color="#FAFAFA",
            corner_radius=0,
            scrollbar_button_color="#DDDDDD",
            scrollbar_button_hover_color="#BBBBBB"
        )
        self.panel_catalogo.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # Panel derecho — carrito
        self._construir_carrito(cuerpo)

    # ────────────────────────────────────────────────────────────────────
    def _construir_carrito(self, parent):
        panel = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#EBEBEB",
            width=240
        )
        panel.pack(side="right", fill="y", padx=(0, 0))
        panel.pack_propagate(False)

        ctk.CTkLabel(
            panel, text="🛒  Mi Carrito",
            font=("Georgia", 15, "bold"),
            text_color="#1A1A1A"
        ).pack(pady=(18, 6), padx=16)

        ctk.CTkFrame(panel, fg_color="#EBEBEB", height=1).pack(fill="x", padx=16)

        # Lista de items del carrito
        self.scroll_carrito = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent",
            height=280,
            scrollbar_button_color="#DDDDDD"
        )
        self.scroll_carrito.pack(fill="x", padx=10, pady=8)

        ctk.CTkFrame(panel, fg_color="#EBEBEB", height=1).pack(fill="x", padx=16)

        # Total
        self.lbl_total = ctk.CTkLabel(
            panel,
            text="Total:  $0.00",
            font=("Arimo", 14, "bold"),
            text_color="#1A1A1A"
        )
        self.lbl_total.pack(pady=(10, 6), padx=16)

        # Botón confirmar
        ctk.CTkButton(
            panel,
            text="Confirmar Compra",
            fg_color="#c14b4f",
            hover_color="#dd838e",
            text_color="#FFFFFF",
            font=("Arimo", 13, "bold"),
            height=38,
            corner_radius=10,
            command=self._confirmar_compra
        ).pack(fill="x", padx=16, pady=(0, 8))

        # Botón vaciar
        ctk.CTkButton(
            panel,
            text="Vaciar carrito",
            fg_color="transparent",
            text_color="#999999",
            hover_color="#F5F5F5",
            font=("Arimo", 12),
            height=30,
            command=self._vaciar_carrito
        ).pack(fill="x", padx=16, pady=(0, 14))

    # ════════════════════════════════════════════════════════════════════
    # CATÁLOGO
    # ════════════════════════════════════════════════════════════════════
    def _poblar_catalogo(self, productos: list):
        """Destruye las tarjetas actuales y dibuja las nuevas."""
        for widget in self.panel_catalogo.winfo_children():
            widget.destroy()
        self._img_refs.clear()

        if not productos:
            ctk.CTkLabel(
                self.panel_catalogo,
                text="Sin resultados.",
                font=("Arimo", 14),
                text_color="#AAAAAA"
            ).grid(row=0, column=0, columnspan=COLS, pady=40)
            return

        for idx, prod in enumerate(productos):
            fila = idx // COLS
            col  = idx % COLS
            self._crear_tarjeta(prod, fila, col)

    # ────────────────────────────────────────────────────────────────────
    def _crear_tarjeta(self, prod: dict, fila: int, col: int):
        tarjeta = ctk.CTkFrame(
            self.panel_catalogo,
            fg_color="#FFFFFF",
            corner_radius=14,
            border_width=1,
            border_color="#EBEBEB",
            width=200,
            height=280
        )
        tarjeta.grid(row=fila, column=col, padx=10, pady=10, sticky="nsew")
        tarjeta.grid_propagate(False)

        # Imagen del producto
        img_ctk = self._cargar_imagen(prod["ruta_imagen"], size=(150, 150))
        lbl_img = ctk.CTkLabel(tarjeta, image=img_ctk, text="")
        lbl_img.image = img_ctk          # ← referencia obligatoria
        lbl_img.pack(pady=(16, 6))
        self._img_refs[prod["id"]] = img_ctk

        # Nombre
        ctk.CTkLabel(
            tarjeta,
            text=prod["nombre"],
            font=("Georgia", 12, "bold"),
            text_color="#1A1A1A",
            wraplength=170
        ).pack(padx=10)

        # Precio
        ctk.CTkLabel(
            tarjeta,
            text=f"${prod['precio']:.2f}",
            font=("Arimo", 13),
            text_color="#c14b4f"
        ).pack(pady=(2, 0))

        # Stock
        color_stock = "#27AE60" if prod["stock"] > 0 else "#E74C3C"
        txt_stock   = f"Stock: {prod['stock']}" if prod["stock"] > 0 else "Agotado"
        ctk.CTkLabel(
            tarjeta,
            text=txt_stock,
            font=("Arimo", 10),
            text_color=color_stock
        ).pack()

        # Botones
        btns = ctk.CTkFrame(tarjeta, fg_color="transparent")
        btns.pack(pady=(6, 10), padx=10, fill="x")

        ctk.CTkButton(
            btns,
            text="+ Carrito",
            fg_color="#1A1A1A",
            hover_color="#333333",
            text_color="#FFFFFF",
            font=("Arimo", 11, "bold"),
            height=30,
            corner_radius=8,
            state="normal" if prod["stock"] > 0 else "disabled",
            command=lambda p=prod: self._agregar_carrito(p)
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        # Botón "Probar" solo si tiene color definido y no es 0-0-0
        if prod.get("color_bgr", "0-0-0") != "0-0-0":
            ctk.CTkButton(
                btns,
                text="👄",
                fg_color="#FFF0F0",
                hover_color="#FFD6D6",
                text_color="#c14b4f",
                font=("Arimo", 14),
                width=32,
                height=30,
                corner_radius=8,
                command=lambda p=prod: self._probar_en_tester(p)
            ).pack(side="right")

    # ────────────────────────────────────────────────────────────────────
    def _cargar_imagen(self, ruta_relativa: str, size=(150, 150)) -> ctk.CTkImage:
        """Carga una imagen desde la ruta del producto. Si no existe, muestra placeholder."""
        ruta_abs = os.path.join(self.ruta_base, ruta_relativa)
        try:
            img = Image.open(ruta_abs).convert("RGBA")
        except (FileNotFoundError, Exception):
            # Placeholder de color sólido si la imagen no existe todavía
            img = Image.new("RGBA", size, PLACEHOLDER_COLOR)

        return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    # ════════════════════════════════════════════════════════════════════
    # BÚSQUEDA Y ORDENAMIENTO
    # ════════════════════════════════════════════════════════════════════
    def _on_buscar(self, event=None):
        texto = self.entry_buscar.get().strip().lower()
        if texto:
            # Búsqueda lineal por nombre
            self._visibles = [
                p for p in self._todos
                if texto in p["nombre"].lower()
            ]
        else:
            self._visibles = list(self._todos)
        self._poblar_catalogo(self._visibles)

    # ────────────────────────────────────────────────────────────────────
    def _on_ordenar(self, opcion: str):
        lista = list(self._visibles)

        if opcion == "Precio ↑":
            # Quicksort ascendente por precio
            self._quicksort(lista, 0, len(lista) - 1, "precio", ascendente=True)
        elif opcion == "Precio ↓":
            self._quicksort(lista, 0, len(lista) - 1, "precio", ascendente=False)
        elif opcion == "A → Z":
            # Mergesort por nombre A→Z
            lista = self._mergesort(lista, "nombre", ascendente=True)
        elif opcion == "Z → A":
            lista = self._mergesort(lista, "nombre", ascendente=False)

        self._visibles = lista
        self._poblar_catalogo(self._visibles)

    # ════════════════════════════════════════════════════════════════════
    # ALGORITMOS DE ORDENAMIENTO (llamarán a estructuras/ cuando esté listo)
    # ════════════════════════════════════════════════════════════════════
    def _quicksort(self, lista, bajo, alto, clave, ascendente=True):
        if bajo < alto:
            pi = self._partition(lista, bajo, alto, clave, ascendente)
            self._quicksort(lista, bajo, pi - 1, clave, ascendente)
            self._quicksort(lista, pi + 1, alto, clave, ascendente)

    def _partition(self, lista, bajo, alto, clave, ascendente):
        pivote = lista[alto][clave]
        i = bajo - 1
        for j in range(bajo, alto):
            cond = lista[j][clave] <= pivote if ascendente else lista[j][clave] >= pivote
            if cond:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
        lista[i + 1], lista[alto] = lista[alto], lista[i + 1]
        return i + 1

    def _mergesort(self, lista, clave, ascendente=True):
        if len(lista) <= 1:
            return lista
        mid = len(lista) // 2
        izq = self._mergesort(lista[:mid], clave, ascendente)
        der = self._mergesort(lista[mid:], clave, ascendente)
        return self._merge(izq, der, clave, ascendente)

    def _merge(self, izq, der, clave, ascendente):
        resultado = []
        i = j = 0
        while i < len(izq) and j < len(der):
            cond = izq[i][clave] <= der[j][clave] if ascendente else izq[i][clave] >= der[j][clave]
            if cond:
                resultado.append(izq[i]); i += 1
            else:
                resultado.append(der[j]); j += 1
        resultado.extend(izq[i:])
        resultado.extend(der[j:])
        return resultado

    # ════════════════════════════════════════════════════════════════════
    # CARRITO
    # ════════════════════════════════════════════════════════════════════
    def _agregar_carrito(self, prod: dict):
        self._carrito.append(dict(prod))
        self._refrescar_carrito()

    def _vaciar_carrito(self):
        self._carrito.clear()
        self._refrescar_carrito()

    def _confirmar_compra(self):
        if not self._carrito:
            return
        # Aquí llamarás a carrito_ctrl.confirmar_compra() cuando esté el backend
        self._carrito.clear()
        self._refrescar_carrito()
        # Mostrar confirmación
        ventana = ctk.CTkToplevel(self)
        ventana.title("")
        ventana.geometry("380x180")
        ventana.resizable(False, False)
        ventana.grab_set()
        ctk.CTkLabel(
            ventana,
            text="✓  Orden Confirmada",
            font=("Georgia", 18, "bold"),
            text_color="#27AE60"
        ).pack(pady=(36, 8))
        ctk.CTkLabel(
            ventana,
            text="Se ha enviado un correo con el detalle\nde tu compra.",
            font=("Arimo", 13),
            text_color="#555555"
        ).pack()
        ventana.after(2800, ventana.destroy)

    def _refrescar_carrito(self):
        for w in self.scroll_carrito.winfo_children():
            w.destroy()

        for item in self._carrito:
            fila = ctk.CTkFrame(self.scroll_carrito, fg_color="transparent")
            fila.pack(fill="x", pady=2)
            ctk.CTkLabel(
                fila,
                text=item["nombre"],
                font=("Arimo", 11),
                text_color="#333333",
                wraplength=130,
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(
                fila,
                text=f"${item['precio']:.2f}",
                font=("Arimo", 11, "bold"),
                text_color="#c14b4f"
            ).pack(side="right")

        total = sum(i["precio"] for i in self._carrito)
        self.lbl_total.configure(text=f"Total:  ${total:.2f}")

    # ════════════════════════════════════════════════════════════════════
    # TESTER
    # ════════════════════════════════════════════════════════════════════
    def _probar_en_tester(self, prod: dict):
        """
        Navega al frame de Asesoría y le pasa el color del producto.
        Cuando FrameAsesoria esté implementado, descomentar la línea de abajo.
        """
        # self.app.mostrar_frame("asesoria", color_bgr=prod["color_bgr"])
        print(f"[Tester] Probando {prod['nombre']} con color {prod['color_bgr']}")