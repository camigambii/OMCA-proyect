# gui/frame_asesoria.py
import customtkinter as ctk
from PIL import Image
import os
import queue # <--- Importante para leer los frames de tu worker
import config

from backend.camara_worker import CamaraWorker # Importamos tu clase real

COLOR_ROSA = "#c14b4f"        
COLOR_NEGRO = "#0F0C0C"       
COLOR_BLANCO = "#FFFFFF"      
COLOR_GRIS_FONDO = "#FAFAFA"  

class FrameAsesoria(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BLANCO, corner_radius=0)
        self.app = app
        self.ruta_base = os.path.dirname(os.path.dirname(__file__))
        self.pack_propagate(False)

        self._img_refs = {}

        self._construir_ui()

        self.frame_queue = queue.Queue(maxsize=2)
        
        
        self.worker = CamaraWorker(self.frame_queue)
        
        
        self.app.registrar_worker(self.worker)
        
        
        self.worker.start()
        
        
        self.actualizar_frame()

    def _construir_ui(self):
        ctk.CTkLabel(
            self, text="A S E S O R Í A  V I R T U A L", font=("Georgia", 20, "bold"), text_color=COLOR_NEGRO
        ).pack(pady=(22, 4))

        ctk.CTkLabel(
            self, text="Prueba en vivo y descubre tu tono ideal", font=("Arimo", 12), text_color="#888888"
        ).pack(pady=(0, 20))

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=540)
        self.left_frame.pack(side="left", fill="y", padx=(0, 15))
        self.left_frame.pack_propagate(False)

        self.camera_frame = ctk.CTkFrame(self.left_frame, fg_color="#EAEAEA", corner_radius=15, width=500, height=500)
        self.camera_frame.pack(pady=(0, 20))
        self.camera_frame.pack_propagate(False)

        self.camera_label = ctk.CTkLabel(
            self.camera_frame, text="Encendiendo cámara...", font=("Arimo", 14), text_color="#555555"
        )
        self.camera_label.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.left_frame, text="Prueba Rápida (Labiales):", font=("Arimo", 12, "bold"), text_color=COLOR_NEGRO
        ).pack(anchor="w", pady=(0, 10))

        self.colors_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.colors_frame.pack(fill="x")


        self.crear_boton_color("#FF6B81", 255, 107, 129)
        self.crear_boton_color("#C06C84", 192, 108, 132)
        self.crear_boton_color("#E17055", 225, 112, 85)
        self.crear_boton_color("#c14b4f", 193, 75, 79)   


        ctk.CTkButton(
            self.colors_frame, text="Limpiar Cara", fg_color="transparent", border_width=1, border_color="#DDDDDD", 
            text_color=COLOR_NEGRO, height=40, corner_radius=20, command=self.limpiar_cara
        ).pack(side="left", padx=10)

        self.right_frame = ctk.CTkFrame(
            self.main_frame, fg_color=COLOR_BLANCO, corner_radius=15, border_width=1, border_color="#EBEBEB"
        )
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.rec_title = ctk.CTkLabel(
            self.right_frame, text="RECOMENDACIONES PARA TI", font=("Georgia", 16, "bold"), text_color=COLOR_NEGRO
        )
        self.rec_title.pack(pady=(20, 10))

        ctk.CTkFrame(self.right_frame, fg_color="#EBEBEB", height=1).pack(fill="x", padx=20)

        self.scroll_recomendaciones = ctk.CTkScrollableFrame(
            self.right_frame, fg_color="transparent", scrollbar_button_color="#DDDDDD"
        )
        self.scroll_recomendaciones.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_productos_recomendados()

    def actualizar_frame(self):
        """Saca imágenes de la cola del worker y las pone en la pantalla"""
        if not self.frame_queue.empty():
            try:
                img_pil = self.frame_queue.get_nowait()
                
                img_ctk = ctk.CTkImage(light_image=img_pil, size=(500, 375)) 
                self.camera_label.configure(image=img_ctk, text="")
            except queue.Empty:
                pass
        
        
        if hasattr(self, 'worker') and self.worker.corriendo:
            self.after(15, self.actualizar_frame)


    def crear_boton_color(self, hex_color, r, g, b):
        btn = ctk.CTkButton(
            self.colors_frame, text="", width=40, height=40, corner_radius=20,
            fg_color=hex_color, hover_color=hex_color, border_width=1, border_color="#DDDDDD",
            command=lambda r=r, g=g, b=b: self.probar_color(r, g, b, "gloss")
        )
        btn.pack(side="left", padx=(0, 10))

    def probar_color(self, r, g, b, categoria):
        try:

            self.worker.cambiar_maquillaje(b, g, r, categoria)
        except Exception as e:
            print(f"Error al cambiar maquillaje: {e}")

    def limpiar_cara(self):
        try:
            self.worker.limpiar_maquillaje()
        except Exception as e:
            pass


    def cargar_productos_recomendados(self):
        inventario_completo = config.arbol_inventario.obtener_lista_inorden()
        productos_recomendados = []

        color_usuario = getattr(config, "COLORIMETRIA_ACTUAL", None)

        for prod in inventario_completo:
            try:
                digito_color = int(str(prod.id)[0])
                if digito_color == 3 or color_usuario is None or digito_color == color_usuario:
                    if "accesorios" not in prod.categoria.lower():
                        productos_recomendados.append(prod)
            except:
                continue

        for prod in productos_recomendados[:10]:
            self.crear_card_recomendacion(prod)

        if not productos_recomendados:
            ctk.CTkLabel(self.scroll_recomendaciones, text="No hay recomendaciones.", font=("Arimo", 14), text_color="#AAAAAA").pack(pady=40)

    def crear_card_recomendacion(self, prod):
        card = ctk.CTkFrame(self.scroll_recomendaciones, fg_color=COLOR_GRIS_FONDO, border_width=1, border_color="#EBEBEB", corner_radius=12)
        card.pack(fill="x", padx=10, pady=8)

        ruta_abs = os.path.join(self.ruta_base, prod.ruta_imagen)
        try:
            img_pil = Image.open(ruta_abs).convert("RGBA")
        except:
            img_pil = Image.new("RGBA", (80, 80), "#F0ECE8")
            
        img_ctk = ctk.CTkImage(light_image=img_pil, size=(80, 80))
        self._img_refs[prod.id] = img_ctk 

        ctk.CTkLabel(card, image=img_ctk, text="").pack(side="left", padx=15, pady=15)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=15)

        ctk.CTkLabel(info_frame, text=prod.nombre, font=("Georgia", 14, "bold"), text_color=COLOR_NEGRO, anchor="w").pack(fill="x")
        ctk.CTkLabel(info_frame, text=prod.categoria.capitalize(), font=("Arimo", 11), text_color="#888888", anchor="w").pack(fill="x")
        ctk.CTkLabel(info_frame, text=f"${prod.precio:.2f}", font=("Arimo", 13, "bold"), text_color=COLOR_ROSA, anchor="w").pack(fill="x", pady=(5, 0))


        if not (prod.color_r == 0 and prod.color_g == 0 and prod.color_b == 0):
            val_b, val_g, val_r = prod.obtener_rgb()
            cat = prod.categoria.strip().lower()
            ctk.CTkButton(
                card, text="👄 Probar", fg_color=COLOR_NEGRO, hover_color="#333333", text_color=COLOR_BLANCO,
                font=("Arimo", 12, "bold"), width=90, height=32, corner_radius=8,
                command=lambda r=val_r, g=val_g, b=val_b, c=cat: self.probar_color(r, g, b, c) 
            ).pack(side="right", padx=20)


    def detener_camara(self):
        try:
            if hasattr(self, 'worker') and self.worker:
                self.worker.detener()
        except:
            pass

    def destroy(self):
        self.detener_camara()
        super().destroy()