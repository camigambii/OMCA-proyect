
import customtkinter as ctk
from PIL import Image
import os


# Importamos los frames (descomentarlos conforme los vayas creando)
from gui.menu_principal import MenuPrincipal
from gui.frame_gloss    import FrameGloss
# from gui.frames.frame_rubor    import FrameRubor
# from gui.frames.frame_paletas  import FramePaletas
# from gui.frames.frame_bronzer  import FrameBronzer
# from gui.frames.frame_asesoria import FrameAsesoria
# from gui.frames.frame_login    import FrameLogin
# from gui.frames.frame_admin    import FrameAdmin

ANCHO  = 1100
ALTO   = 1100
ALTO_HEADER = 90


class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ── Configuración de la ventana ──────────────────────────────────
        self.title("OMCA")
        self.geometry(f"{ANCHO}x{ALTO}")
        self.minsize(ANCHO, ALTO)
        self.maxsize(ANCHO, ALTO)          # tamaño fijo, no se puede redimensionar
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")

        self.ruta_base = os.path.dirname(os.path.dirname(__file__))

        # ── Cargar logo ──────────────────────────────────────────────────
        img_logo = Image.open(
            os.path.join(self.ruta_base, "assets", "interfaz", "logo_omca.png")
        )
        self.logo_image = ctk.CTkImage(
            light_image=img_logo,
            dark_image=img_logo,
            size=(220, 65)
        )

        # ── Referencia al frame activo y al worker de cámara ─────────────
        self.frame_actual   = None
        self.camara_worker  = None   # se llena cuando FrameAsesoria está activo

        self._construir_ui()

    # ────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN DE LA UI
    # ────────────────────────────────────────────────────────────────────
    def _construir_ui(self):
        # ── HEADER ──────────────────────────────────────────────────────
        self.header = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            height=ALTO_HEADER,
            border_width=0
        )
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Línea separadora sutil debajo del header
        self.separador = ctk.CTkFrame(
            self, fg_color="#E8E8E8", corner_radius=0, height=1
        )
        self.separador.pack(fill="x", side="top")

        # Logo
        ctk.CTkLabel(
            self.header, image=self.logo_image, text=""
        ).pack(side="left", padx=30, pady=12)

        # ── Botón REGRESAR (derecha del header, oculto al inicio) ────────
        self.btn_regresar = ctk.CTkButton(
            self.header,
            text="← MENÚ",
            fg_color="transparent",
            text_color="#555555",
            hover_color="#F5F5F5",
            font=("Arimo", 12),
            width=80,
            command=lambda: self.mostrar_frame("menu")
        )
        # No se hace pack aquí; se muestra/oculta dinámicamente

        # ── Nav central ─────────────────────────────────────────────────
        self.nav = ctk.CTkFrame(self.header, fg_color="transparent")
        self.nav.pack(side="left", expand=True, padx=10)

        estilo_nav = {
            "fg_color": "transparent",
            "text_color": "#0F0C0C",
            "hover_color": "#F5F5F5",
            "font": ("Arimo", 14, "bold"),
            "width": 110,
            "height": 36,
            "corner_radius": 6,
        }

        estilo_asesoria = {
            "fg_color": "#c14b4f",
            "text_color": "#FFFFFF",
            "hover_color": "#dd838e",
            "font": ("Arimo", 14, "bold"),
            "width": 110,
            "height": 36,
            "corner_radius": 20,
        }

        # Guardamos referencias a los botones de nav para poder
        # resaltarlos cuando la sección está activa
        self.btn_login = ctk.CTkButton(
            self.nav, text="INICIAR SESIÓN", **estilo_nav,
            command=lambda: self.mostrar_frame("login")
        )
        self.btn_login.pack(side="left", padx=6)

        self.btn_gloss = ctk.CTkButton(
            self.nav, text="GLOSS", **estilo_nav,
            command=lambda: self.mostrar_frame("gloss")
        )
        self.btn_gloss.pack(side="left", padx=6)

        self.btn_rubor = ctk.CTkButton(
            self.nav, text="RUBOR", **estilo_nav,
            command=lambda: self.mostrar_frame("rubor")
        )
        self.btn_rubor.pack(side="left", padx=6)

        self.btn_paletas = ctk.CTkButton(
            self.nav, text="PALETAS", **estilo_nav,
            command=lambda: self.mostrar_frame("paletas")
        )
        self.btn_paletas.pack(side="left", padx=6)

        self.btn_bronzer = ctk.CTkButton(
            self.nav, text="BRONZER", **estilo_nav,
            command=lambda: self.mostrar_frame("bronzer")
        )
        self.btn_bronzer.pack(side="left", padx=6)

        self.btn_asesoria = ctk.CTkButton(
            self.nav, text="ASESORÍA", **estilo_asesoria,
            command=lambda: self.mostrar_frame("asesoria")
        )
        self.btn_asesoria.pack(side="left", padx=12)

        # ── CONTENEDOR PRINCIPAL ─────────────────────────────────────────
        # Aquí viven todos los frames de navegación
        self.contenedor = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            width=ANCHO,
            height=ALTO - ALTO_HEADER - 1   # -1 por el separador
        )
        self.contenedor.pack(fill="both", expand=True)
        self.contenedor.pack_propagate(False)

        # ── Arrancar en el menú principal ────────────────────────────────
        self.mostrar_frame("menu")

    # ────────────────────────────────────────────────────────────────────
    # NAVEGACIÓN CENTRAL
    # ────────────────────────────────────────────────────────────────────
    def mostrar_frame(self, nombre: str):
        """
        Destruye el frame actual y carga el nuevo dentro de self.contenedor.
        Si el frame activo es FrameAsesoria, detiene la cámara antes de destruir.
        """

        # 1. Limpiar frame anterior
        if self.frame_actual is not None:
            # Si hay cámara activa, detenerla antes de destruir el frame
            if self.camara_worker is not None:
                self.camara_worker.detener()
                self.camara_worker = None
            self.frame_actual.destroy()
            self.frame_actual = None

        # 2. Mapa de frames disponibles
        #    Descomentar cada línea conforme vayas creando los archivos
        mapa = {
            "menu":     MenuPrincipal,
            "gloss":    FrameGloss,
            # "rubor":    FrameRubor,
            # "paletas":  FramePaletas,
            # "bronzer":  FrameBronzer,
            # "asesoria": FrameAsesoria,
            # "login":    FrameLogin,
            # "admin":    FrameAdmin,
        }

        if nombre not in mapa:
            print(f"[AppWindow] Frame '{nombre}' aún no implementado.")
            nombre = "menu"

        # 3. Instanciar y mostrar
        ClaseFrame = mapa[nombre]
        self.frame_actual = ClaseFrame(self.contenedor, self)
        self.frame_actual.pack(fill="both", expand=True)

        # 4. Mostrar / ocultar botón regresar
        if nombre == "menu":
            self.btn_regresar.pack_forget()
        else:
            self.btn_regresar.pack(side="right", padx=20)

        # 5. Resaltar botón activo en la nav
        self._actualizar_nav_activa(nombre)

    # ────────────────────────────────────────────────────────────────────
    # RESALTAR BOTÓN ACTIVO EN NAV
    # ────────────────────────────────────────────────────────────────────
    def _actualizar_nav_activa(self, nombre: str):
        """Subraya / resalta el botón de la sección activa."""
        mapa_botones = {
            "login":    self.btn_login,
            "gloss":    self.btn_gloss,
            "rubor":    self.btn_rubor,
            "paletas":  self.btn_paletas,
            "bronzer":  self.btn_bronzer,
            "asesoria": self.btn_asesoria,
        }

        # Resetear todos a estilo normal
        for key, btn in mapa_botones.items():
            if key == "asesoria":
                btn.configure(fg_color="#c14b4f", text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color="#0F0C0C")

        # Resaltar el activo
        if nombre in mapa_botones and nombre != "asesoria":
            mapa_botones[nombre].configure(
                fg_color="#F0F0F0",
                text_color="#c14b4f"
            )

    # ────────────────────────────────────────────────────────────────────
    # HELPERS PARA LOS FRAMES HIJOS
    # ────────────────────────────────────────────────────────────────────
    def registrar_worker(self, worker):
        """FrameAsesoria llama a esto para registrar su hilo de cámara."""
        self.camara_worker = worker

    def actualizar_btn_sesion(self, usuario_activo):
        """
        FrameLogin llama a esto cuando el login es exitoso.
        Cambia el botón de 'INICIAR SESIÓN' a 'Hola, {username}'.
        Si el usuario es admin, muestra botón extra de ADMIN.
        """
        if usuario_activo is None:
            self.btn_login.configure(
                text="INICIAR SESIÓN",
                command=lambda: self.mostrar_frame("login")
            )
        else:
            self.btn_login.configure(
                text=f"Hola, {usuario_activo.username}",
                command=lambda: self.mostrar_frame("login")
            )