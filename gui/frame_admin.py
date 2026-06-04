# gui/frame_admin.py
import customtkinter as ctk
import config
from backend import auth_manager, inventario_ctrl
from estructuras.ordenamiento import quicksort, mergesort, radix_sort, bubblesort
from estructuras.busqueda import busqueda_binaria


class FrameAdmin(ctk.CTkFrame):
    """
    Panel del administrador con dos pestañas:
    - Inventario: gestión completa de productos
    - Usuarios: ver y eliminar usuarios
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#FAFAFA", corner_radius=0)
        self.app = app
        self._construir()

    # ════════════════════════════════════════════════════════════════════
    def _construir(self):
        ctk.CTkLabel(
            self, text="PANEL DE ADMINISTRADOR",
            font=("Georgia", 20, "bold"), text_color="#1A1A1A"
        ).pack(pady=(18, 12))

        tabs = ctk.CTkTabview(self, fg_color="#FFFFFF", segmented_button_fg_color="#EBEBEB",
                              segmented_button_selected_color="#c14b4f",
                              segmented_button_selected_hover_color="#dd838e",
                              text_color="#1A1A1A")
        tabs.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        tabs.add("Inventario")
        tabs.add("Usuarios")

        self._construir_inventario(tabs.tab("Inventario"))
        self._construir_usuarios(tabs.tab("Usuarios"))

    # ════════════════════════════════════════════════════════════════════
    # PESTAÑA INVENTARIO
    # ════════════════════════════════════════════════════════════════════
    def _construir_inventario(self, tab):
        # ── Formulario superior ─────────────────────────────────────────
        form = ctk.CTkFrame(tab, fg_color="#FFFFFF", corner_radius=10,
                            border_width=1, border_color="#EBEBEB")
        form.pack(fill="x", padx=10, pady=(10, 8))

        # Fila 1: ID, Nombre, Categoría
        fila1 = ctk.CTkFrame(form, fg_color="transparent")
        fila1.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(fila1, text="ID:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.entry_id = ctk.CTkEntry(fila1, width=80, height=32, placeholder_text="10001")
        self.entry_id.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(fila1, text="Nombre:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.entry_nombre = ctk.CTkEntry(fila1, width=180, height=32, placeholder_text="Nombre del producto")
        self.entry_nombre.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(fila1, text="Categoría:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.opt_cat = ctk.CTkOptionMenu(
            fila1, values=["gloss", "rubor", "paleta", "bronzer", "accesorios"],
            font=("Arimo", 12), width=140, height=32
        )
        self.opt_cat.pack(side="left", padx=(4, 0))

        # Fila 2: Precio, Stock, Ruta imagen
        fila2 = ctk.CTkFrame(form, fg_color="transparent")
        fila2.pack(fill="x", padx=12, pady=(4, 4))

        ctk.CTkLabel(fila2, text="Precio:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.entry_precio = ctk.CTkEntry(fila2, width=90, height=32, placeholder_text="0.00")
        self.entry_precio.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(fila2, text="Stock:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.entry_stock = ctk.CTkEntry(fila2, width=80, height=32, placeholder_text="0")
        self.entry_stock.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(fila2, text="Ruta imagen:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.entry_ruta = ctk.CTkEntry(fila2, width=220, height=32, placeholder_text="assets/productos/nombre.png")
        self.entry_ruta.pack(side="left", padx=(4, 16))

        # Fila 3: RGB
        fila3 = ctk.CTkFrame(form, fg_color="transparent")
        fila3.pack(fill="x", padx=12, pady=(4, 4))

        for lbl, attr in [("R:", "entry_r"), ("G:", "entry_g"), ("B:", "entry_b")]:
            ctk.CTkLabel(fila3, text=lbl, font=("Arimo", 12), text_color="#555555").pack(side="left")
            e = ctk.CTkEntry(fila3, width=60, height=32, placeholder_text="0")
            e.pack(side="left", padx=(4, 12))
            setattr(self, attr, e)

        # Fila 4: botones de acción
        fila4 = ctk.CTkFrame(form, fg_color="transparent")
        fila4.pack(fill="x", padx=12, pady=(4, 10))

        estilo_btn = {"font": ("Arimo", 12, "bold"), "height": 34, "corner_radius": 8}

        ctk.CTkButton(fila4, text="Agregar Producto", fg_color="#27AE60", hover_color="#1e8449",
                      **estilo_btn, command=self._agregar_producto).pack(side="left", padx=(0, 8))

        ctk.CTkButton(fila4, text="Agregar Stock", fg_color="#2980B9", hover_color="#1a6691",
                      **estilo_btn, command=self._agregar_stock).pack(side="left", padx=(0, 8))

        ctk.CTkButton(fila4, text="Borrar Producto", fg_color="#c0392b", hover_color="#922b21",
                      **estilo_btn, command=self._borrar_producto).pack(side="left", padx=(0, 8))

        ctk.CTkButton(fila4, text="Borrar Stock", fg_color="#e67e22", hover_color="#ca6f1e",
                      **estilo_btn, command=self._borrar_stock).pack(side="left", padx=(0, 8))

        # Búsqueda por ID
        fila5 = ctk.CTkFrame(form, fg_color="transparent")
        fila5.pack(fill="x", padx=12, pady=(0, 10))

        ctk.CTkLabel(fila5, text="Buscar por ID exacto:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.entry_buscar_id = ctk.CTkEntry(fila5, width=100, height=32, placeholder_text="10001")
        self.entry_buscar_id.pack(side="left", padx=(4, 8))
        ctk.CTkButton(fila5, text="Buscar", font=("Arimo", 12), height=32,
                      fg_color="#555555", hover_color="#333333",
                      command=self._buscar_por_id).pack(side="left")

        self.lbl_msg_inv = ctk.CTkLabel(fila5, text="", font=("Arimo", 11), text_color="#c14b4f")
        self.lbl_msg_inv.pack(side="left", padx=12)

        # Ordenamiento
        fila_ord = ctk.CTkFrame(tab, fg_color="transparent")
        fila_ord.pack(fill="x", padx=10, pady=(0, 6))

        ctk.CTkLabel(fila_ord, text="Ordenar tabla:", font=("Arimo", 12), text_color="#555555").pack(side="left")
        self.opt_orden_inv = ctk.CTkOptionMenu(
            fila_ord,
            values=["Por ID (Radix Sort)", "Por Nombre (Mergesort)", "Por Precio (Quicksort)", "Por Categoría (Bubblesort)"],
            font=("Arimo", 12), width=240, height=32, command=self._ordenar_inventario
        )
        self.opt_orden_inv.pack(side="left", padx=8)

        # Tabla de productos
        self.scroll_inventario = ctk.CTkScrollableFrame(
            tab, fg_color="#FFFFFF", corner_radius=10,
            border_width=1, border_color="#EBEBEB"
        )
        self.scroll_inventario.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Encabezados
        enc = ctk.CTkFrame(self.scroll_inventario, fg_color="#F5F5F5", corner_radius=0)
        enc.pack(fill="x", pady=(0, 2))
        for txt, w in [("ID", 80), ("Nombre", 200), ("Categoría", 110), ("Precio", 90), ("Stock", 70)]:
            ctk.CTkLabel(enc, text=txt, font=("Arimo", 11, "bold"), text_color="#555555", width=w, anchor="w").pack(side="left", padx=6)

        self._contenedor_filas_inv = ctk.CTkFrame(self.scroll_inventario, fg_color="transparent")
        self._contenedor_filas_inv.pack(fill="x")

        self._refrescar_inventario()

    def _refrescar_inventario(self, productos=None):
        for w in self._contenedor_filas_inv.winfo_children():
            w.destroy()

        if productos is None:
            productos = inventario_ctrl.obtenerTodosProductos()

        for i, prod in enumerate(productos):
            bg = "#FAFAFA" if i % 2 == 0 else "#FFFFFF"
            fila = ctk.CTkFrame(self._contenedor_filas_inv, fg_color=bg, corner_radius=0, height=32)
            fila.pack(fill="x", pady=1)
            fila.pack_propagate(False)

            for val, w in [(str(prod.id), 80), (prod.nombre, 200), (prod.categoria, 110),
                           (f"${prod.precio:.2f}", 90), (str(prod.stock), 70)]:
                ctk.CTkLabel(fila, text=val, font=("Arimo", 11), text_color="#333333",
                             width=w, anchor="w").pack(side="left", padx=6)

    def _agregar_producto(self):
        try:
            pid = int(self.entry_id.get())
            nombre = self.entry_nombre.get().strip()
            cat = self.opt_cat.get()
            precio = float(self.entry_precio.get())
            stock = int(self.entry_stock.get())
            ruta = self.entry_ruta.get().strip()
            r = int(self.entry_r.get() or 0)
            g = int(self.entry_g.get() or 0)
            b = int(self.entry_b.get() or 0)
        except ValueError:
            self.lbl_msg_inv.configure(text="Datos inválidos", text_color="#c14b4f")
            return

        from estructuras.arboles import Producto
        nodo = config.arbol_inventario.buscar(pid)
        if nodo is not None:
            self.lbl_msg_inv.configure(text="ID ya existe", text_color="#c14b4f")
            return

        nuevo = Producto(pid, nombre, cat, precio, stock, ruta, b, g, r)
        config.arbol_inventario.insertar(nuevo)
        config.persistence_manager.guardarProductos(config.arbol_inventario)
        self.lbl_msg_inv.configure(text="Producto agregado", text_color="#27AE60")
        self._refrescar_inventario()

    def _agregar_stock(self):
        try:
            pid = int(self.entry_id.get())
            cantidad = int(self.entry_stock.get())
        except ValueError:
            self.lbl_msg_inv.configure(text="ID y Stock requeridos", text_color="#c14b4f")
            return
        ok = inventario_ctrl.agregarStock(pid, cantidad)
        self.lbl_msg_inv.configure(
            text="✓ Stock actualizado" if ok else "⚠ Producto no encontrado",
            text_color="#27AE60" if ok else "#c14b4f"
        )
        self._refrescar_inventario()

    def _borrar_producto(self):
        try:
            pid = int(self.entry_id.get())
        except ValueError:
            self.lbl_msg_inv.configure(text="ID requerido", text_color="#c14b4f")
            return
        ok = inventario_ctrl.borrarProducto(pid)
        self.lbl_msg_inv.configure(
            text="✓ Producto eliminado" if ok else "⚠ No encontrado",
            text_color="#27AE60" if ok else "#c14b4f"
        )
        self._refrescar_inventario()

    def _borrar_stock(self):
        try:
            pid = int(self.entry_id.get())
            cantidad = int(self.entry_stock.get())
        except ValueError:
            self.lbl_msg_inv.configure(text="ID y Stock requeridos", text_color="#c14b4f")
            return
        ok = inventario_ctrl.borrarStock(pid, cantidad)
        self.lbl_msg_inv.configure(
            text="✓ Stock reducido" if ok else "Stock insuficiente o no encontrado",
            text_color="#27AE60" if ok else "#c14b4f"
        )
        self._refrescar_inventario()

    def _buscar_por_id(self):
        try:
            pid = int(self.entry_buscar_id.get())
        except ValueError:
            self.lbl_msg_inv.configure(text="ID inválido", text_color="#c14b4f")
            return
        nodo = config.arbol_inventario.buscar(pid)
        if nodo is None:
            self.lbl_msg_inv.configure(text="No encontrado", text_color="#c14b4f")
        else:
            prod = nodo.producto
            self.lbl_msg_inv.configure(text=f" {prod.nombre} — ${prod.precio:.2f} (Stock: {prod.stock})", text_color="#27AE60")

    def _ordenar_inventario(self, opcion):
        lista = inventario_ctrl.obtenerTodosProductos()
        if "Radix" in opcion:
            lista = radix_sort(lista)
        elif "Mergesort" in opcion:
            lista = mergesort(lista, clave="nombre")
        elif "Quicksort" in opcion:
            quicksort(lista, 0, len(lista) - 1, clave="precio")
        elif "Bubblesort" in opcion:
            bubblesort(lista, clave="categoria")
        self._refrescar_inventario(lista)

    # ════════════════════════════════════════════════════════════════════
    # PESTAÑA USUARIOS
    # ════════════════════════════════════════════════════════════════════
    def _construir_usuarios(self, tab):
        ctk.CTkLabel(
            tab, text="Usuarios registrados en el sistema",
            font=("Arimo", 13), text_color="#777777"
        ).pack(pady=(12, 8))

        self.lbl_msg_usr = ctk.CTkLabel(tab, text="", font=("Arimo", 11), text_color="#c14b4f")
        self.lbl_msg_usr.pack()

        # Encabezado
        enc = ctk.CTkFrame(tab, fg_color="#F5F5F5", corner_radius=0, height=30)
        enc.pack(fill="x", padx=10)
        enc.pack_propagate(False)
        for txt, w in [("Usuario", 200), ("Rol", 120)]:
            ctk.CTkLabel(enc, text=txt, font=("Arimo", 11, "bold"), text_color="#555555",
                         width=w, anchor="w").pack(side="left", padx=8)

        self.scroll_usuarios = ctk.CTkScrollableFrame(
            tab, fg_color="#FFFFFF", corner_radius=10,
            border_width=1, border_color="#EBEBEB"
        )
        self.scroll_usuarios.pack(fill="both", expand=True, padx=10, pady=(2, 10))

        self._refrescar_usuarios()

    def _refrescar_usuarios(self):
        for w in self.scroll_usuarios.winfo_children():
            w.destroy()

        usuarios = config.tabla_hash.obtener_todos()
        # Bubblesort manual por username (los usuarios no son Producto)
        n = len(usuarios)
        for i in range(n):
            for j in range(0, n - i - 1):
                if usuarios[j].username.lower() > usuarios[j + 1].username.lower():
                    usuarios[j], usuarios[j + 1] = usuarios[j + 1], usuarios[j]

        for i, usr in enumerate(usuarios):
            bg = "#FAFAFA" if i % 2 == 0 else "#FFFFFF"
            fila = ctk.CTkFrame(self.scroll_usuarios, fg_color=bg, corner_radius=0, height=34)
            fila.pack(fill="x", pady=1)
            fila.pack_propagate(False)

            ctk.CTkLabel(fila, text=usr.username, font=("Arimo", 12), text_color="#333333",
                         width=200, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(fila, text=usr.rol, font=("Arimo", 12), text_color="#666666",
                         width=120, anchor="w").pack(side="left", padx=8)

            # No mostrar botón eliminar para el usuario activo
            es_yo = (config.USUARIO_ACTIVO and usr.username == config.USUARIO_ACTIVO.username)
            ctk.CTkButton(
                fila, text="Eliminar", fg_color="#c0392b" if not es_yo else "#CCCCCC",
                hover_color="#922b21" if not es_yo else "#CCCCCC",
                font=("Arimo", 11), height=26, width=80,
                state="disabled" if es_yo else "normal",
                command=lambda u=usr.username: self._eliminar_usuario(u)
            ).pack(side="right", padx=8)

    def _eliminar_usuario(self, username):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Confirmar")
        ventana.geometry("360x160")
        ventana.grab_set()

        ctk.CTkLabel(ventana, text=f"¿Eliminar al usuario '{username}'?",
                     font=("Arimo", 14), text_color="#1A1A1A").pack(pady=(30, 12))

        btns = ctk.CTkFrame(ventana, fg_color="transparent")
        btns.pack()

        def confirmar():
            ok = auth_manager.eliminar_usuario(username)
            self.lbl_msg_usr.configure(
                text=f"✓ '{username}' eliminado" if ok else "⚠ Error al eliminar",
                text_color="#27AE60" if ok else "#c14b4f"
            )
            ventana.destroy()
            self._refrescar_usuarios()

        ctk.CTkButton(btns, text="Sí, eliminar", fg_color="#c0392b", hover_color="#922b21",
                      font=("Arimo", 12), command=confirmar).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="Cancelar", fg_color="#888888", hover_color="#666666",
                      font=("Arimo", 12), command=ventana.destroy).pack(side="left", padx=8)

