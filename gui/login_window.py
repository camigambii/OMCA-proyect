# gui/login_window.py

import customtkinter as ctk

from backend import auth_manager

# =========================================================
# IMPORTAR VISTAS
# =========================================================

# IMPORTANTE:
# Estas clases deben existir después.
# Por ahora puedes comentarlas si aún no las creas.

# from gui.admin_view import VistaAdmin
# from gui.user_view import VistaUsuario


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

ctk.set_appearance_mode("dark")

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

        self.geometry("500x600")

        self.resizable(False, False)

        # =================================================
        # TÍTULO / LOGO
        # =================================================

        self.logo_label = ctk.CTkLabel(
            self,
            text="OMCA",
            font=("Arial", 32, "bold")
        )

        self.logo_label.pack(pady=(40, 10))

        # =================================================
        # SUBTÍTULO
        # =================================================

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Iniciar Sesión",
            font=("Arial", 22)
        )

        self.subtitle_label.pack(pady=(10, 30))

        # =================================================
        # ENTRY USUARIO
        # =================================================

        self.username_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Usuario"
        )

        self.username_entry.pack(pady=10)

        # =================================================
        # ENTRY PASSWORD
        # =================================================

        self.password_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Contraseña",
            show="*"
        )

        self.password_entry.pack(pady=10)

        # =================================================
        # LABEL ERROR
        # =================================================

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red"
        )

        self.error_label.pack(pady=5)

        # =================================================
        # BOTÓN LOGIN
        # =================================================

        self.login_button = ctk.CTkButton(
            self,
            text="Iniciar Sesión",
            width=300,
            command=self.iniciar_sesion
        )

        self.login_button.pack(pady=20)

        # =================================================
        # BOTÓN REGISTRO
        # =================================================

        self.register_button = ctk.CTkButton(
            self,
            text="¿No tienes cuenta? Regístrate",
            width=300,
            fg_color="gray25",
            hover_color="gray35",
            command=self.mostrar_registro
        )

        self.register_button.pack(pady=10)

        # =================================================
        # COMPONENTES REGISTRO
        # =================================================

        self.confirm_password_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Confirmar contraseña",
            show="*"
        )

        self.create_account_button = ctk.CTkButton(
            self,
            text="Crear Cuenta",
            width=300,
            command=self.crear_cuenta
        )

        self.back_button = ctk.CTkButton(
            self,
            text="Volver al Login",
            width=300,
            fg_color="gray25",
            hover_color="gray35",
            command=self.ocultar_registro
        )

    # =====================================================
    # MOSTRAR PANEL REGISTRO
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

        self.error_label.configure(text="")

    # =====================================================
    # OCULTAR PANEL REGISTRO
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

        self.error_label.configure(text="")

    # =====================================================
    # LOGIN
    # =====================================================

    def iniciar_sesion(self):

        username = (
            self.username_entry.get().strip()
        )

        password = (
            self.password_entry.get().strip()
        )

        # =============================================
        # VALIDAR CAMPOS
        # =============================================

        if username == "" or password == "":

            self.error_label.configure(
                text="Completa todos los campos"
            )

            return

        # =============================================
        # LOGIN
        # =============================================

        resultado = auth_manager.login(
            username,
            password
        )

        # =============================================
        # ADMIN
        # =============================================

        if resultado == "admin":

            self.destroy()

            print(
                "Abrir VistaAdmin"
            )

            # vista = VistaAdmin()
            # vista.mainloop()

        # =============================================
        # CLIENTE
        # =============================================

        elif resultado == "cliente":

            self.destroy()

            print(
                "Abrir VistaUsuario"
            )

            # vista = VistaUsuario()
            # vista.mainloop()

        # =============================================
        # ERROR LOGIN
        # =============================================

        else:

            self.error_label.configure(
                text=(
                    "Usuario o contraseña "
                    "incorrectos"
                )
            )

    # =====================================================
    # REGISTRO
    # =====================================================

    def crear_cuenta(self):

        username = (
            self.username_entry.get().strip()
        )

        password = (
            self.password_entry.get().strip()
        )

        confirm_password = (
            self.confirm_password_entry
            .get()
            .strip()
        )

        # =============================================
        # VALIDAR CAMPOS VACÍOS
        # =============================================

        if (
            username == ""
            or password == ""
            or confirm_password == ""
        ):

            self.error_label.configure(
                text="Completa todos los campos"
            )

            return

        # =============================================
        # VALIDAR PASSWORDS
        # =============================================

        if password != confirm_password:

            self.error_label.configure(
                text=(
                    "Las contraseñas "
                    "no coinciden"
                )
            )

            return

        # =============================================
        # REGISTRAR
        # =============================================

        resultado = auth_manager.registrar(
            username,
            password
        )

        # =============================================
        # REGISTRO EXITOSO
        # =============================================

        if resultado:

            self.error_label.configure(
                text="Cuenta creada exitosamente",
                text_color="green"
            )

            # Limpiar campos

            self.username_entry.delete(0, "end")

            self.password_entry.delete(0, "end")

            self.confirm_password_entry.delete(
                0,
                "end"
            )

            # Volver al login

            self.after(
                1500,
                self.ocultar_registro
            )

        # =============================================
        # USUARIO EXISTENTE
        # =============================================

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
