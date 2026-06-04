# gui/frames/frame_gloss.py
import customtkinter as ctk
from PIL import Image
import os
import config
from estructuras.ordenamiento import quicksort, mergesort
from backend.carrito_ctrl import (
    agregar_al_carrito,
    quitar_del_carrito,
    obtener_carrito,
    calcular_total,
    confirmarCompra,
    vaciarCarrito
)

PLACEHOLDER_COLOR = "#F0ECE8"
COLS = 3

class FrameGloss(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#FAFAFA", corner_radius=0)
        self.app = app
        self.ruta_base = os.path.dirname(os.path.dirname(__file__))

        # =========================================================
        # CONEXIÓN AL BACKEND REAL (ÁRBOL BST)
        # =========================================================
        inventario_completo = config.arbol_inventario.obtener_lista_inorden()

        self._todos = []
        for p in inventario_completo:
            if p.categoria.lower() == "gloss":
                self._todos.append(p)

        self._visibles = list(self._todos)
        self._img_refs = {}

        self._construir()
        self._poblar_catalogo(self._visibles)

    # ════════════════════════════════════════════════════════════════════
    # CONSTRUCCIÓN DE LA UI
    # ════════════════════════════════════════════════════════════════════
    def _construir(self):
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

        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(fill="x", padx=30, pady=(0, 12))

        self.entry_buscar = ctk.CTkEntry(
            barra,
            placeholder_text="🔍  Buscar producto...",
            font=("Arimo", 13),
            width=240,
            height=36,
            corner_radius=18,
            fg_color="#FFFFFF"
        )
        self.entry_buscar.pack(side="left", padx=(0, 12))
        self.entry_buscar.bind("<KeyRelease>", self._on_buscar)

        ctk.CTkLabel(
            barra, text="Ordenar:", font=("Arimo", 12), text_color="#666666"
        ).pack(side="left", padx=(0, 6))

        self.opt_orden = ctk.CTkOptionMenu(
            barra,
            values=["Precio ↑", "Precio ↓", "A → Z", "Z → A"],
            font=("Arimo", 12),
            width=130,
            height=36,
            fg_color="#FFFFFF",
            text_color="#333333",
            command=self._on_ordenar
        )
        self.opt_orden.pack(side="left")

        cuerpo = ctk.CTkFrame(self, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.panel_catalogo = ctk.CTkScrollableFrame(
            cuerpo, fg_color="#FAFAFA", corner_radius=0
        )
        self.panel_catalogo.pack(side="left", fill="both", expand=True, padx=(0, 12))

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
        panel.pack(side="right", fill="y")
        panel.pack_propagate(False)

        ctk.CTkLabel(
            panel, text="🛒  Mi Carrito",
            font=("Georgia", 15, "bold"),
            text_color="#1A1A1A"
        ).pack(pady=(18, 6), padx=16)

        ctk.CTkFrame(panel, fg_color="#EBEBEB", height=1).pack(fill="x", padx=16)

        self.scroll_carrito = ctk.CTkScrollableFrame(
            panel, fg_color="transparent", height=280
        )
        self.scroll_carrito.pack(fill="x", padx=10, pady=8)

        ctk.CTkFrame(panel, fg_color="#EBEBEB", height=1).pack(fill="x", padx=16)

        self.lbl_total = ctk.CTkLabel(
            panel, text="Total:  $0.00",
            font=("Arimo", 14, "bold"),
            text_color="#1A1A1A"
        )
        self.lbl_total.pack(pady=(10, 6), padx=16)

        ctk.CTkButton(
            panel,
            text="Confirmar Compra",
            fg_color="#dd838e",
            hover_color="#c96f7b",
            font=("Arimo", 13, "bold"),
            height=38,
            command=self._confirmar_compra
        ).pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkButton(
            panel,
            text="Vaciar carrito",
            fg_color="transparent",
            text_color="#999999",
            hover_color="#F5F5F5",
            command=self._vaciar_carrito
        ).pack(fill="x", padx=16, pady=(0, 14))

    # ════════════════════════════════════════════════════════════════════
    # CATÁLOGO
    # ════════════════════════════════════════════════════════════════════
    def _poblar_catalogo(self, productos: list):
        for widget in self.panel_catalogo.winfo_children():
            widget.destroy()
        self._img_refs.clear()

        if not productos:
            ctk.CTkLabel(
                self.panel_catalogo,
                text="No hay productos en esta categoría.",
                font=("Arimo", 14),
                text_color="#AAAAAA"
            ).grid(row=0, column=0, columnspan=COLS, pady=40)
            return

        for idx, prod in enumerate(productos):
            fila = idx // COLS
            col  = idx % COLS
            self._crear_tarjeta(prod, fila, col)

    # ────────────────────────────────────────────────────────────────────
    def _crear_tarjeta(self, prod, fila: int, col: int):
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

        img_ctk = self._cargar_imagen(prod.ruta_imagen, size=(150, 150))
        lbl_img = ctk.CTkLabel(tarjeta, image=img_ctk, text="")
        lbl_img.image = img_ctk
        lbl_img.pack(pady=(16, 6))
        self._img_refs[prod.id] = img_ctk

        ctk.CTkLabel(
            tarjeta, text=prod.nombre,
            font=("Georgia", 12, "bold"),
            text_color="#1A1A1A",
            wraplength=170
        ).pack(padx=10)

        ctk.CTkLabel(
            tarjeta, text=f"${prod.precio:.2f}",
            font=("Arimo", 13),
            text_color="#c14b4f"
        ).pack(pady=(2, 0))

        color_stock = "#27AE60" if prod.stock > 0 else "#E74C3C"
        txt_stock   = f"Stock: {prod.stock}" if prod.stock > 0 else "Agotado"
        ctk.CTkLabel(
            tarjeta, text=txt_stock,
            font=("Arimo", 10),
            text_color=color_stock
        ).pack()

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
            state="normal" if prod.stock > 0 else "disabled",
            command=lambda p=prod: self._agregar_carrito(p)
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(
            btns,
            text="👄",
            fg_color="#FFF0F0",
            text_color="#dd838e",
            font=("Arimo", 14),
            width=32,
            height=30,
            corner_radius=8,
            command=lambda p=prod: self._probar_en_tester(p)
        ).pack(side="right")

    # ────────────────────────────────────────────────────────────────────
    def _cargar_imagen(self, ruta_relativa: str, size=(150, 150)):
        ruta_abs = os.path.join(self.ruta_base, ruta_relativa)
        try:
            img = Image.open(ruta_abs).convert("RGBA")
        except Exception:
            img = Image.new("RGBA", size, PLACEHOLDER_COLOR)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    # ════════════════════════════════════════════════════════════════════
    # BÚSQUEDA Y ORDENAMIENTO
    # ════════════════════════════════════════════════════════════════════
    def _on_buscar(self, event=None):
        texto = self.entry_buscar.get().strip().lower()
        if texto:
            self._visibles = [p for p in self._todos if texto in p.nombre.lower()]
        else:
            self._visibles = list(self._todos)
        self._poblar_catalogo(self._visibles)

    # ────────────────────────────────────────────────────────────────────
    def _on_ordenar(self, opcion: str):
        lista = list(self._visibles)

        if opcion == "Precio ↑":
            quicksort(lista, 0, len(lista) - 1, clave="precio")
        elif opcion == "Precio ↓":
            quicksort(lista, 0, len(lista) - 1, clave="precio")
            lista.reverse()
        elif opcion == "A → Z":
            lista = mergesort(lista, clave="nombre")
        elif opcion == "Z → A":
            lista = mergesort(lista, clave="nombre")
            lista.reverse()

        self._visibles = lista
        self._poblar_catalogo(self._visibles)

    # ════════════════════════════════════════════════════════════════════
    # CARRITO — usa carrito_ctrl.py del backend
    # ════════════════════════════════════════════════════════════════════
    def _agregar_carrito(self, prod):
        agregar_al_carrito(prod)
        self._refrescar_carrito()

    def _vaciar_carrito(self):
        vaciarCarrito()
        self._refrescar_carrito()

    def _confirmar_compra(self):
        if not obtener_carrito():
            return
        confirmarCompra()
        self._refrescar_carrito()
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
            font=("Arimo", 13)
        ).pack()
        ventana.after(2800, ventana.destroy)

    def _refrescar_carrito(self):
        for w in self.scroll_carrito.winfo_children():
            w.destroy()

        for item in obtener_carrito():
            fila = ctk.CTkFrame(self.scroll_carrito, fg_color="transparent")
            fila.pack(fill="x", pady=2)
            ctk.CTkLabel(
                fila, text=item.nombre,
                font=("Arimo", 11),
                wraplength=130,
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(
                fila, text=f"${item.precio:.2f}",
                font=("Arimo", 11, "bold"),
                text_color="#c14b4f"
            ).pack(side="right")

        self.lbl_total.configure(text=f"Total:  ${calcular_total():.2f}")

    # ════════════════════════════════════════════════════════════════════
    # TESTER
    # ════════════════════════════════════════════════════════════════════
    def _probar_en_tester(self, prod):
        print(f"[Tester] Probando {prod.nombre} con Color: {prod.color_bgr}")
        # self.app.mostrar_frame("asesoria")