# gui/login_window.py

import customtkinter as ctk

from PIL import Image

from backend import auth_manager


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

ctk.set_appearance_mode("light")

ctk.set_default_color_theme("blue")


# =========================================================
# LOGIN WINDOW
# =========================================================

class LoginWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        # =================================================
        # CONFIGURAR VENTANA
        # =================================================

        self.title("OMCA - Login")

        self.geometry("500x650")

        self.resizable(False, False)

        self.configure(
            fg_color="#F8F4F0"
        )

        # =================================================
        # LOGO PNG
        # =================================================

        self.logo_image = ctk.CTkImage(
            light_image=Image.open(
                "assets/logo.png"
            ),
            size=(180, 180)
        )

        self.logo_label = ctk.CTkLabel(
            self,
            text="",
            image=self.logo_image
        )

        self.logo_label.pack(
            pady=(30, 10)
        )

        # =================================================
        # TÍTULO
        # =================================================

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Iniciar Sesión",
            font=("Yu Gothic UI Semibold", 24),
            text_color="#2B2B2B"
        )

        self.subtitle_label.pack(
            pady=(10, 30)
        )

        # =================================================
        # ENTRY USUARIO
        # =================================================

        self.username_entry = ctk.CTkEntry(
            self,
            width=320,
            height=45,
            placeholder_text="Usuario",
            font=("Yu Gothic UI Semibold", 15)
        )

        self.username_entry.pack(
            pady=10
        )

        # =================================================
        # ENTRY PASSWORD
        # =================================================

        self.password_entry = ctk.CTkEntry(
            self,
            width=320,
            height=45,
            placeholder_text="Contraseña",
            show="*",
            font=("Yu Gothic UI Semibold", 15)
        )

        self.password_entry.pack(
            pady=10
        )

        # =================================================
        # LABEL ERROR
        # =================================================

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            font=("Yu Gothic UI Semibold", 14),
            text_color="red"
        )

        self.error_label.pack(
            pady=5
        )

        # =================================================
        # BOTÓN LOGIN
        # =================================================

        self.login_button = ctk.CTkButton(
            self,
            text="Iniciar Sesión",
            width=320,
            height=40,
            command=self.iniciar_sesion
        )

        self.login_button.pack(
            pady=20
        )

        # =================================================
        # BOTÓN REGISTRO
        # =================================================

        self.register_button = ctk.CTkButton(
            self,
            text="¿No tienes cuenta? Regístrate",
            width=320,
            height=40,
            fg_color="#C7A17A",
            hover_color="#B08B65",
            command=self.mostrar_registro
        )

        self.register_button.pack(
            pady=10
        )

        # =================================================
        # COMPONENTES REGISTRO
        # =================================================

        self.confirm_password_entry = ctk.CTkEntry(
            self,
            width=320,
            height=45,
            placeholder_text="Confirmar contraseña",
            show="*",
            font=("Yu Gothic UI Semibold", 15)
        )

        self.create_account_button = ctk.CTkButton(
            self,
            text="Crear Cuenta",
            width=320,
            height=40,
            command=self.crear_cuenta
        )

        self.back_button = ctk.CTkButton(
            self,
            text="Volver al Login",
            width=320,
            height=40,
            fg_color="gray50",
            hover_color="gray40",
            command=self.ocultar_registro
        )

    # =====================================================
    # MOSTRAR REGISTRO
    # =====================================================

    def mostrar_registro(self):

        self.subtitle_label.configure(
            text="Crear Cuenta"
        )

        self.confirm_password_entry.pack(
            pady=10
        )

        self.create_account_button.pack(
            pady=10
        )

        self.back_button.pack(
            pady=10
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

        self.subtitle_label.configure(
            text="Iniciar Sesión"
        )

        self.confirm_password_entry.pack_forget()

        self.create_account_button.pack_forget()

        self.back_button.pack_forget()

        self.login_button.pack(
            pady=20
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
                text="Completa todos los campos",
                text_color="red"
            )

            return

        # =================================================
        # LOGIN
        # =================================================

        resultado = auth_manager.login(
            username,
            password
        )

        print(
            "Resultado login:",
            resultado
        )

        # =================================================
        # ADMIN
        # =================================================

        if resultado == "admin":

            self.destroy()

            print(
                "Abrir VistaAdmin"
            )

            # from gui.admin_view import VistaAdmin

            # vista = VistaAdmin()

            # vista.mainloop()

        # =================================================
        # CLIENTE
        # =================================================

        elif resultado == "cliente":

            self.destroy()

            print(
                "Abrir VistaUsuario"
            )

            # from gui.user_view import VistaUsuario

            # vista = VistaUsuario()

            # vista.mainloop()

        # =================================================
        # ERROR LOGIN
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
        # REGISTRO EXITOSO
        # =================================================

        if resultado:

            self.error_label.configure(
                text=(
                    "Cuenta creada "
                    "exitosamente"
                ),
                text_color="green"
            )

            # =============================================
            # LIMPIAR CAMPOS
            # =============================================

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

            # =============================================
            # REGRESAR AL LOGIN
            # =============================================

            self.after(
                1500,
                self.ocultar_registro
            )

        # =================================================
        # USUARIO YA EXISTE
        # =================================================

        else:

            self.error_label.configure(
                text=(
                    "Ese nombre de usuario "
                    "ya existe"
                ),
                text_color="red"
            )


# =========================================================
# EJECUCIÓN DIRECTA
# =========================================================

if __name__ == "__main__":

    ventana = LoginWindow()

    ventana.mainloop()
