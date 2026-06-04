import customtkinter as ctk
from PIL import Image

import config

from backend import camara_worker
from backend import inventario_ctrl


COLOR_ROSA = "#dd838e"
COLOR_NEGRO = "#0F0C0C"
COLOR_BLANCO = "#FFFFFF"


class FrameAsesoria(ctk.CTkFrame):

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
        # TÍTULO
        # =================================================

        self.title_label = ctk.CTkLabel(
            self,
            text="ASESORÍA VIRTUAL",
            font=("Yu Gothic UI Semibold", 34),
            text_color=COLOR_NEGRO
        )

        self.title_label.pack(
            pady=(20, 10)
        )

        # =================================================
        # CONTENEDOR
        # =================================================

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_BLANCO
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # =================================================
        # PANEL IZQUIERDO
        # =================================================

        self.left_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLOR_BLANCO,
            width=520
        )

        self.left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.left_frame.pack_propagate(False)

        # =================================================
        # CÁMARA
        # =================================================

        self.camera_label = ctk.CTkLabel(
            self.left_frame,
            text="Iniciando cámara...",
            width=500,
            height=500,
            fg_color="#EAEAEA",
            text_color=COLOR_NEGRO,
            corner_radius=15,
            font=("Yu Gothic UI Semibold", 18)
        )

        self.camera_label.pack(
            pady=10
        )

        # =================================================
        # BOTONES COLORES
        # =================================================

        self.colors_frame = ctk.CTkFrame(
            self.left_frame,
            fg_color=COLOR_BLANCO
        )

        self.colors_frame.pack(
            pady=20
        )

        self.crear_boton("#FF6B81", 255, 107, 129)
        self.crear_boton("#C06C84", 192, 108, 132)
        self.crear_boton("#F67280", 246, 114, 128)
        self.crear_boton("#6C5CE7", 108, 92, 231)
        self.crear_boton("#E17055", 225, 112, 85)

        # =================================================
        # PANEL DERECHO
        # =================================================

        self.right_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#F7F7F7",
            corner_radius=20
        )

        self.right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10
        )

        # =================================================
        # TÍTULO RECOMENDACIONES
        # =================================================

        self.rec_title = ctk.CTkLabel(
            self.right_frame,
            text="RECOMENDACIONES",
            font=("Yu Gothic UI Semibold", 28),
            text_color=COLOR_NEGRO
        )

        self.rec_title.pack(
            pady=(20, 10)
        )

        # =================================================
        # SCROLL PRODUCTOS
        # =================================================

        self.scroll = ctk.CTkScrollableFrame(
            self.right_frame,
            width=400,
            height=700,
            fg_color=COLOR_BLANCO
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # =================================================
        # INICIAR CÁMARA
        # =================================================

        try:

            camara_worker.iniciar_camara(
                self.camera_label
            )

        except:

            self.camera_label.configure(
                text="No se pudo iniciar cámara"
            )

        # =================================================
        # CARGAR PRODUCTOS
        # =================================================

        self.cargar_productos()

    # =====================================================
    # BOTÓN COLOR
    # =====================================================

    def crear_boton(self, color, r, g, b):

        boton = ctk.CTkButton(
            self.colors_frame,
            text="",
            width=60,
            height=60,
            corner_radius=30,
            fg_color=color,
            hover_color=color,
            border_width=2,
            border_color=COLOR_NEGRO,
            command=lambda:
            self.probar_color(r, g, b)
        )

        boton.pack(
            side="left",
            padx=8
        )

    # =====================================================
    # PROBAR COLOR
    # =====================================================

    def probar_color(self, r, g, b):

        try:

            camara_worker.cambiar_color(
                r,
                g,
                b
            )

        except:

            pass

    # =====================================================
    # CARGAR PRODUCTOS
    # =====================================================

    def cargar_productos(self):

        productos = (
            inventario_ctrl
            .obtenerTodosProductos()
        )

        for producto in productos:

            codigo = str(producto.id)

            colorimetria = int(codigo[0])

            if (
                hasattr(
                    config,
                    "COLORIMETRIA_ACTUAL"
                )
            ):

                if (
                    colorimetria != 3
                    and
                    colorimetria
                    !=
                    config.COLORIMETRIA_ACTUAL
                ):

                    continue

            self.crear_card(producto)

    # =====================================================
    # CARD PRODUCTO
    # =====================================================

    def crear_card(self, producto):

        card = ctk.CTkFrame(
            self.scroll,
            fg_color=COLOR_BLANCO,
            border_width=2,
            border_color=COLOR_ROSA,
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        content = ctk.CTkFrame(
            card,
            fg_color=COLOR_BLANCO
        )

        content.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # =================================================
        # IMAGEN
        # =================================================

        try:

            imagen = ctk.CTkImage(
                light_image=Image.open(
                    producto.ruta_imagen
                ),
                size=(100, 100)
            )

            img_label = ctk.CTkLabel(
                content,
                image=imagen,
                text=""
            )

            img_label.pack(
                side="left",
                padx=10
            )

        except:

            img_label = ctk.CTkLabel(
                content,
                text="Sin imagen",
                width=100,
                height=100
            )

            img_label.pack(
                side="left",
                padx=10
            )

        # =================================================
        # INFO
        # =================================================

        info = ctk.CTkFrame(
            content,
            fg_color=COLOR_BLANCO
        )

        info.pack(
            side="left",
            padx=10,
            fill="both",
            expand=True
        )

        nombre = ctk.CTkLabel(
            info,
            text=producto.nombre,
            font=("Yu Gothic UI Semibold", 22),
            text_color=COLOR_NEGRO
        )

        nombre.pack(
            anchor="w"
        )

        categoria = ctk.CTkLabel(
            info,
            text=producto.categoria,
            font=("Yu Gothic UI Semibold", 16),
            text_color=COLOR_NEGRO
        )

        categoria.pack(
            anchor="w"
        )

        precio = ctk.CTkLabel(
            info,
            text=f"${producto.precio}",
            font=("Yu Gothic UI Semibold", 18),
            text_color=COLOR_ROSA
        )

        precio.pack(
            anchor="w"
        )

    # =====================================================
    # DETENER CÁMARA
    # =====================================================

    def detener_camara(self):

        try:

            camara_worker.detener()

        except:

            pass

    # =====================================================
    # DESTROY
    # =====================================================

    def destroy(self):

        self.detener_camara()

        super().destroy()

