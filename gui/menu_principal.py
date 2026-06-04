# gui/frames/menu_principal.py
import customtkinter as ctk
from PIL import Image
import os


class MenuPrincipal(ctk.CTkFrame):
    """
    Frame de inicio — muestra la imagen hero (portada.png) ocupando
    todo el contenedor de forma responsiva.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        self.app       = app          # referencia a AppWindow
        self.ruta_base = os.path.dirname(
            os.path.dirname(__file__)
        )

        # Cargar imagen hero
        self.hero_pil = Image.open(
            os.path.join(self.ruta_base, "assets", "interfaz", "portada.png")
        )
        self.hero_ctk = None

        self._construir()
        # Esperar a que el frame tenga dimensiones reales antes de dibujar
        self.after(50, self._dibujar_hero)
        self.bind("<Configure>", self._on_resize)

    # ────────────────────────────────────────────────────────────────────
    def _construir(self):
        self.hero_label = ctk.CTkLabel(self, text="")
        self.hero_label.place(relx=0.5, rely=0.5, anchor="center")

    # ────────────────────────────────────────────────────────────────────
    def _on_resize(self, event):
        if event.widget is self:
            self._dibujar_hero()

    # ────────────────────────────────────────────────────────────────────
    def _dibujar_hero(self):
        ancho = self.winfo_width()
        alto  = self.winfo_height()

        if ancho < 10 or alto < 10:
            return

        img_w, img_h = self.hero_pil.size
        escala  = min(ancho / img_w, alto / img_h)
        nuevo_w = int(img_w * escala)
        nuevo_h = int(img_h * escala)

        img_resized = self.hero_pil.resize((nuevo_w, nuevo_h), Image.LANCZOS)

        self.hero_ctk = ctk.CTkImage(
            light_image=img_resized,
            dark_image=img_resized,
            size=(nuevo_w, nuevo_h)
        )
        self.hero_label.configure(
            image=self.hero_ctk,
            width=nuevo_w,
            height=nuevo_h
        )