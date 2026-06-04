import customtkinter as ctk
from tkinter import messagebox

from backend import inventario_ctrl
from backend import auth_manager

import config


COLOR_ROSA = "#dd838e"
COLOR_NEGRO = "#0F0C0C"
COLOR_BLANCO = "#FFFFFF"


class FrameVistaAdmin(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(
            parent,
            width=1100,
            height=1100,
            fg_color=COLOR_BLANCO
        )

        self.app = app

        self.pack_propagate(False)

        # =================================================
        # TABVIEW
        # =================================================

        self.tabs = ctk.CTkTabview(
            self,
            width=1000,
            height=950,
            fg_color=COLOR_BLANCO,
            segmented_button_fg_color=COLOR_ROSA,
            segmented_button_selected_color=COLOR_NEGRO
        )

        self.tabs.pack(
            pady=20,
            padx=20,
            fill="both",
            expand=True
        )

        self.tabs.add("Inventario")
        self.tabs.add("Usuarios")

        self.tab_inventario = self.tabs.tab("Inventario")
        self.tab_usuarios = self.tabs.tab("Usuarios")

        self.crear_inventario()
        self.crear_usuarios()

    # =====================================================
    # INVENTARIO
    # =====================================================

    def crear_inventario(self):

        self.id_entry = ctk.CTkEntry(
            self.tab_inventario,
            placeholder_text="ID"
        )

        self.id_entry.pack(pady=5)

        self.nombre_entry = ctk.CTkEntry(
            self.tab_inventario,
            placeholder_text="Nombre"
        )

        self.nombre_entry.pack(pady=5)

        self.categoria_menu = ctk.CTkOptionMenu(
            self.tab_inventario,
            values=[
                "Gloss",
                "Rubor",
                "Paleta",
                "Bronzer"
            ]
        )

        self.categoria_menu.pack(pady=5)

        self.precio_entry = ctk.CTkEntry(
            self.tab_inventario,
            placeholder_text="Precio"
        )

        self.precio_entry.pack(pady=5)

        self.stock_entry = ctk.CTkEntry(
            self.tab_inventario,
            placeholder_text="Stock"
        )

        self.stock_entry.pack(pady=5)

        self.ruta_entry = ctk.CTkEntry(
            self.tab_inventario,
            placeholder_text="Ruta imagen"
        )

        self.ruta_entry.pack(pady=5)

        # =================================================
        # BOTONES
        # =================================================

        self.buttons_frame = ctk.CTkFrame(
            self.tab_inventario,
            fg_color=COLOR_BLANCO
        )

        self.buttons_frame.pack(
            pady=15
        )

        self.add_button = ctk.CTkButton(
            self.buttons_frame,
            text="Agregar Producto",
            fg_color=COLOR_ROSA,
            text_color=COLOR_NEGRO,
            command=self.agregar_producto
        )

        self.add_button.pack(
            side="left",
            padx=5
        )

        self.stock_button = ctk.CTkButton(
            self.buttons_frame,
            text="Agregar Stock",
            fg_color=COLOR_ROSA,
            text_color=COLOR_NEGRO,
            command=self.agregar_stock
        )

        self.stock_button.pack(
            side="left",
            padx=5
        )

        self.delete_button = ctk.CTkButton(
            self.buttons_frame,
            text="Borrar Producto",
            fg_color="#c14b4f",
            text_color=COLOR_BLANCO,
            command=self.borrar_producto
        )

        self.delete_button.pack(
            side="left",
            padx=5
        )

        self.remove_stock_button = ctk.CTkButton(
            self.buttons_frame,
            text="Borrar Stock",
            fg_color="#c14b4f",
            text_color=COLOR_BLANCO,
            command=self.borrar_stock
        )

        self.remove_stock_button.pack(
            side="left",
            padx=5
        )

        # =================================================
        # TABLA
        # =================================================

        self.scroll = ctk.CTkScrollableFrame(
            self.tab_inventario,
            width=900,
            height=450
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.refrescar_tabla()

    # =====================================================
    # USUARIOS
    # =====================================================

    def crear_usuarios(self):

        self.users_scroll = ctk.CTkScrollableFrame(
            self.tab_usuarios,
            width=900,
            height=700
        )

        self.users_scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.refrescar_usuarios()

    # =====================================================
    # AGREGAR PRODUCTO
    # =====================================================

    def agregar_producto(self):

        resultado = (
            inventario_ctrl
            .agregar_producto(
                int(self.id_entry.get()),
                self.nombre_entry.get(),
                self.categoria_menu.get(),
                float(self.precio_entry.get()),
                int(self.stock_entry.get()),
                self.ruta_entry.get()
            )
        )

        if resultado:

            self.refrescar_tabla()

    # =====================================================
    # AGREGAR STOCK
    # =====================================================

    def agregar_stock(self):

        inventario_ctrl.agregarStock(
            int(self.id_entry.get()),
            int(self.stock_entry.get())
        )

        self.refrescar_tabla()

    # =====================================================
    # BORRAR PRODUCTO
    # =====================================================

    def borrar_producto(self):

        inventario_ctrl.borrarProducto(
            int(self.id_entry.get())
        )

        self.refrescar_tabla()

    # =====================================================
    # BORRAR STOCK
    # =====================================================

    def borrar_stock(self):

        inventario_ctrl.borrarStock(
            int(self.id_entry.get()),
            int(self.stock_entry.get())
        )

        self.refrescar_tabla()

    # =====================================================
    # REFRESCAR TABLA
    # =====================================================

    def refrescar_tabla(self):

        for widget in self.scroll.winfo_children():

            widget.destroy()

        productos = (
            inventario_ctrl
            .obtenerTodosProductos()
        )

        for producto in productos:

            fila = ctk.CTkFrame(
                self.scroll,
                fg_color=COLOR_BLANCO
            )

            fila.pack(
                fill="x",
                pady=5
            )

            texto = (
                f"{producto.id} | "
                f"{producto.nombre} | "
                f"{producto.categoria} | "
                f"${producto.precio} | "
                f"Stock: {producto.stock}"
            )

            label = ctk.CTkLabel(
                fila,
                text=texto,
                font=("Yu Gothic UI Semibold", 16),
                text_color=COLOR_NEGRO
            )

            label.pack(
                anchor="w",
                padx=10,
                pady=10
            )

    # =====================================================
    # REFRESCAR USUARIOS
    # =====================================================

    def refrescar_usuarios(self):

        for widget in self.users_scroll.winfo_children():

            widget.destroy()

        usuarios = (
            config.tabla_hash.obtener_todos()
        )

        for usuario in usuarios:

            fila = ctk.CTkFrame(
                self.users_scroll,
                fg_color=COLOR_BLANCO
            )

            fila.pack(
                fill="x",
                pady=5
            )

            texto = (
                f"{usuario.username} "
                f"({usuario.rol})"
            )

            label = ctk.CTkLabel(
                fila,
                text=texto,
                font=("Yu Gothic UI Semibold", 16),
                text_color=COLOR_NEGRO
            )

            label.pack(
                side="left",
                padx=10,
                pady=10
            )

            if (
                usuario.username
                !=
                config.USUARIO_ACTIVO.username
            ):

                boton = ctk.CTkButton(
                    fila,
                    text="Eliminar",
                    fg_color="#c14b4f",
                    command=lambda u=usuario:
                    self.eliminar_usuario(
                        u.username
                    )
                )

                boton.pack(
                    side="right",
                    padx=10
                )

    # =====================================================
    # ELIMINAR USUARIO
    # =====================================================

    def eliminar_usuario(self, username):

        confirmacion = (
            messagebox.askyesno(
                "Confirmar",
                f"¿Eliminar a {username}?"
            )
        )

        if confirmacion:

            auth_manager.eliminar_usuario(
                username
            )

            self.refrescar_usuarios()

