# gui/frame_login.py

import customtkinter as ctk

from PIL import Image

from backend import auth_manager

import config


# =========================================================
# COLORES OMCA
# =========================================================

COLOR_ROSA = "#dd838e"

COLOR_NEGRO = "#0F0C0C"

COLOR_BLANCO = "#F0F0F0"


# =========================================================
# FRAME LOGIN
# =========================================================

class FrameLogin(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(
            parent,
            fg_color=COLOR_BLANCO,
            width=1100,
            height=1100
        )

        self.app = app

        self.pack_propagate(False)

        # =================================================
        # CONTENEDOR CENTRAL
        # =================================================

        self.center_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_BLANCO
        )

        self.center_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =================================================
        # LOGO
        # =================================================

        self.logo_image = ctk.CTkImage(
            light_image=Image.open(
                "assets/logo.png"
            ),
            size=(320, 320)
        )

        self.logo_label = ctk.CTkLabel(
            self.center_frame,
            text="",
            image=self.logo_image
        )

        self.logo_label.pack(
            pady=(20, 10)
        )

        # =================================================
        # TÍTULO
        # =================================================

        self.title_label = ctk.CTkLabel(
            self.center_frame,
            text="Iniciar Sesión",
            font=(
                "Yu Gothic UI Semibold",
                36
            ),
            text_color=COLOR_NEGRO
        )

        self.title_label.pack(
            pady=(10, 35)
        )

        # =================================================
        # USERNAME
        # =================================================

        self.username_entry = ctk.CTkEntry(
            self.center_frame,
            width=420,
            height=55,
            placeholder_text="Usuario",
            font=(
                "Yu Gothic UI Semibold",
                18
            ),
            corner_radius=15,
            border_width=2,
            border_color=COLOR_ROSA,
            fg_color=COLOR_BLANCO,
            text_color=COLOR_NEGRO
        )

        self.username_entry.pack(
            pady=12
        )

        # =================================================
        # PASSWORD
        # =================================================

        self.password_entry = ctk.CTkEntry(
            self.center_frame,
            width=420,
            height=55,
            placeholder_text="Contraseña",
            show="*",
            font=(
                "Yu Gothic UI Semibold",
                18
            ),
            corner_radius=15,
            border_width=2,
            border_color=COLOR_ROSA,
            fg_color=COLOR_BLANCO,
            text_color=COLOR_NEGRO
        )

        self.password_entry.pack(
            pady=12
        )

        # =================================================
        # CONFIRM PASSWORD
        # =================================================

        self.confirm_password_entry = (
            ctk.CTkEntry(
                self.center_frame,
                width=420,
                height=55,
                placeholder_text=(
                    "Confirmar contraseña"
                ),
                show="*",
                font=(
                    "Yu Gothic UI Semibold",
                    18
                ),
                corner_radius=15,
                border_width=2,
                border_color=COLOR_ROSA,
                fg_color=COLOR_BLANCO,
                text_color=COLOR_NEGRO
            )
        )

        # =================================================
        # LABEL ERROR
        # =================================================

        self.error_label = ctk.CTkLabel(
            self.center_frame,
            text="",
            font=(
                "Yu Gothic UI Semibold",
                16
            ),
            text_color="red"
        )

        self.error_label.pack(
            pady=8
        )

        # =================================================
        # BOTÓN LOGIN
        # =================================================

        self.login_button = ctk.CTkButton(
            self.center_frame,
            text="Iniciar Sesión",
            width=420,
            height=55,
            fg_color=COLOR_ROSA,
            hover_color="#c96f7b",
            text_color=COLOR_NEGRO,
            font=(
                "Yu Gothic UI Semibold",
                18
            ),
            corner_radius=15,
            command=self.iniciar_sesion
        )

        self.login_button.pack(
            pady=15
        )

        # =================================================
        # BOTÓN REGISTRO
        # =================================================

        self.register_button = ctk.CTkButton(
            self.center_frame,
            text="¿No tienes cuenta? Regístrate",
            width=420,
            height=55,
            fg_color=COLOR_ROSA,
            hover_color="#c96f7b",
            text_color=COLOR_NEGRO,
            font=(
                "Yu Gothic UI Semibold",
                18
            ),
            corner_radius=15,
            command=self.mostrar_registro
        )

        self.register_button.pack(
            pady=10
        )

        # =================================================
        # BOTÓN CREAR CUENTA
        # =================================================

        self.create_account_button = (
            ctk.CTkButton(
                self.center_frame,
                text="Crear Cuenta",
                width=420,
                height=55,
                fg_color=COLOR_ROSA,
                hover_color="#c96f7b",
                text_color=COLOR_NEGRO,
                font=(
                    "Yu Gothic UI Semibold",
                    18
                ),
                corner_radius=15,
                command=self.crear_cuenta
            )
        )

        # =================================================
        # BOTÓN VOLVER
        # =================================================

        self.back_button = ctk.CTkButton(
            self.center_frame,
            text="Volver al Login",
            width=420,
            height=55,
            fg_color=COLOR_NEGRO,
            hover_color="#2A2A2A",
            text_color=COLOR_BLANCO,
            font=(
                "Yu Gothic UI Semibold",
                18
            ),
            corner_radius=15,
            command=self.ocultar_registro
        )

    # =====================================================
    # MOSTRAR REGISTRO
    # =====================================================

    def mostrar_registro(self):

        self.title_label.configure(
            text="Crear Cuenta"
        )

        self.confirm_password_entry.pack(
            pady=12
        )

        self.create_account_button.pack(
            pady=12
        )

        self.back_button.pack(
            pady=12
        )

        self.login_button.pack_forget()

        self.register_button.pack_forget()

        self.error_label.configure(
            text=""
        )

    # =====================================================
    # OCULTAR REGISTRO
    # =====================================================

    def ocultar_registro(self):

        self.title_label.configure(
            text="Iniciar Sesión"
        )

        self.confirm_password_entry.pack_forget()

        self.create_account_button.pack_forget()

        self.back_button.pack_forget()

        self.login_button.pack(
            pady=15
        )

        self.register_button.pack(
            pady=10
        )

        self.error_label.configure(
            text=""
        )

    # =====================================================
    # LOGIN
    # =====================================================

    def iniciar_sesion(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
            .strip()
        )

        # =================================================
        # VALIDAR CAMPOS
        # =================================================

        if username == "" or password == "":

            self.error_label.configure(
                text="Completa todos los campos"
            )

            return

        # =================================================
        # LOGIN
        # =================================================

        resultado = auth_manager.login(
            username,
            password
        )

        # =================================================
        # ADMIN
        # =================================================

        if resultado == "admin":

            self.error_label.configure(
                text="Bienvenido administrador",
                text_color="green"
            )

            self.app.actualizar_navbar()

            self.app.mostrar_frame(
                "menu"
            )

        # =================================================
        # CLIENTE
        # =================================================

        elif resultado == "cliente":

            self.error_label.configure(
                text="Inicio de sesión exitoso",
                text_color="green"
            )

            self.app.actualizar_navbar()

            self.app.mostrar_frame(
                "menu"
            )

        # =================================================
        # ERROR
        # =================================================

        else:

            self.error_label.configure(
                text=(
                    "Usuario o contraseña "
                    "incorrectos"
                ),
                text_color="red"
            )

    # =====================================================
    # CREAR CUENTA
    # =====================================================

    def crear_cuenta(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
            .strip()
        )

        confirm_password = (
            self.confirm_password_entry
            .get()
            .strip()
        )

        # =================================================
        # VALIDAR CAMPOS
        # =================================================

        if (
            username == ""
            or password == ""
            or confirm_password == ""
        ):

            self.error_label.configure(
                text="Completa todos los campos",
                text_color="red"
            )

            return

        # =================================================
        # VALIDAR PASSWORDS
        # =================================================

        if password != confirm_password:

            self.error_label.configure(
                text=(
                    "Las contraseñas "
                    "no coinciden"
                ),
                text_color="red"
            )

            return

        # =================================================
        # REGISTRAR
        # =================================================

        resultado = auth_manager.registrar(
            username,
            password
        )

        # =================================================
        # ÉXITO
        # =================================================

        if resultado:

            self.error_label.configure(
                text=(
                    "Cuenta creada "
                    "exitosamente"
                ),
                text_color="green"
            )

            self.username_entry.delete(
                0,
                "end"
            )

            self.password_entry.delete(
                0,
                "end"
            )

            self.confirm_password_entry.delete(
                0,
                "end"
            )

            self.after(
                1500,
                self.ocultar_registro
            )

        # =================================================
        # ERROR
        # =================================================

        else:

            self.error_label.configure(
                text=(
                    "Ese nombre de usuario "
                    "ya existe"
                ),
                text_color="red"
            )