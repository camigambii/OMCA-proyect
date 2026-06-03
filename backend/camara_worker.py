#GONZAlez pacheco sfoai camila
import cv2
import numpy as np
import mediapipe as mp
from landmarks import FACE_ZONES
import threading
import queue
from PIL import Image

class CamaraWorker(threading.Thread):
    def __init__(self,frame_queue):
        super().__init__(daemon=True)
        self.frame_queue = frame_queue
        self.corriendo = False
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.color_bgr = (0, 0, 0)
        self.alpha_maquillaje = 0.0 
        self.categoria_actual = None
        



    @staticmethod
    def aplicarSombra(frame, face_landmarks, color_bgr, alpha):
        alto, ancho, _ = frame.shape
        overlay = frame.copy()
        rightEye=FACE_ZONES["right_eye"]
        leftEye=FACE_ZONES["left_eye"]
        leftPoints=np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in leftEye
        ], np.int32)

        rightPoints=np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in rightEye
        ], np.int32)

        mask = np.zeros((alto, ancho), dtype=np.uint8)
        cv2.fillPoly(mask, [leftPoints], 255)
        cv2.fillPoly(mask, [rightPoints], 255)
        mask = cv2.GaussianBlur(mask, (21, 21), 0) #impar 

        alpha_mask = (mask / 255.0) * alpha
        alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
        color_layer = np.full((alto, ancho, 3), color_bgr, dtype=np.uint8)
        frame[:] = (frame * (1 - alpha_mask_3c) + color_layer * alpha_mask_3c).astype(np.uint8)



        
    @staticmethod
    def aplicarRubor(frame, face_landmarks, color_bgr, alpha):
        alto, ancho, _ = frame.shape
        overlay = frame.copy()
        leftCheek=FACE_ZONES["left_cheek"]
        rightCheek=FACE_ZONES["right_cheek"]

        left_points = np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in leftCheek
        ], np.int32)
        
        right_points = np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in rightCheek
        ], np.int32)
        
        mask = np.zeros((alto, ancho), dtype=np.uint8)
        cv2.fillPoly(mask, [left_points], 255)
        cv2.fillPoly(mask, [right_points], 255)
        mask = cv2.GaussianBlur(mask, (51, 51), 0) #impar 
        alpha_mask = (mask / 255.0) * alpha
        alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
        color_layer = np.full((alto, ancho, 3), color_bgr, dtype=np.uint8)
        frame[:] = (frame * (1 - alpha_mask_3c) + color_layer * alpha_mask_3c).astype(np.uint8)

    @staticmethod
    def aplicarContour(frame, face_landmarks, color_bgr, alpha):
        alto, ancho, _ = frame.shape
        overlay = frame.copy()
        leftContour=FACE_ZONES["leftContour"]
        rightContour=FACE_ZONES["rightContour"]

        left_points = np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in leftContour
        ], np.int32)
        
        right_points = np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in rightContour
        ], np.int32)
        
        mask = np.zeros((alto, ancho), dtype=np.uint8)
        cv2.fillPoly(mask, [left_points], 255)
        cv2.fillPoly(mask, [right_points], 255)
        mask = cv2.GaussianBlur(mask, (41, 41), 0) #impar
        alpha_mask = (mask / 255.0) * alpha
        alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
        color_layer = np.full((alto, ancho, 3), color_bgr, dtype=np.uint8)
        frame[:] = (frame * (1 - alpha_mask_3c) + color_layer * alpha_mask_3c).astype(np.uint8)


    @staticmethod
    def aplicarLabial(frame, face_landmarks, color_bgr, alpha):
        """Crea una capa de transparencia sobre los labios usando Alpha Blending"""
        alto, ancho, _ = frame.shape
        overlay = frame.copy()
        upper_lip_indices = FACE_ZONES["lips_upper"]
        lower_lip_indices = FACE_ZONES["lips_lower"]

        upper_lip_points = np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in upper_lip_indices
        ], np.int32)
        
        lower_lip_points = np.array([
            [int(face_landmarks.landmark[i].x * ancho), int(face_landmarks.landmark[i].y * alto)] 
            for i in lower_lip_indices
        ], np.int32)

        cv2.fillPoly(overlay, [upper_lip_points], color_bgr)
        cv2.fillPoly(overlay, [lower_lip_points], color_bgr)    
        # Blending
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    def cambiar_maquillaje(self, b, g, r, categoria):
            self.color_bgr = (int(b), int(g), int(r)) 
            self.categoria_actual = categoria.lower()
            self.alpha_maquillaje = 0.4 

    def limpiar_maquillaje(self):
        self.alpha_maquillaje = 0.0
        self.categoria_actual = None

    def detener(self):
        self.corriendo = False


    def run(self):
        self.corriendo=True
        miWebCam = cv2.VideoCapture(1) #------------------------------------------------------------------------------------------------------------------------
        with self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            refine_landmarks=True) as face_mesh:
                
            while self.corriendo:
                ret, frame = miWebCam.read()
                if not ret:
                    break
            
                frame = cv2.flip(frame, 1)
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image_rgb)
                
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        if "gloss" in self.categoria_actual:
                            self.aplicarLabial(frame, face_landmarks, self.color_bgr, self.alpha_maquillaje)
                        elif "rubor" in self.categoria_actual:
                            self.aplicarRubor(frame, face_landmarks, self.color_bgr, self.alpha_maquillaje)
                        elif "paleta" in self.categoria_actual:
                            self.aplicarSombra(frame, face_landmarks, self.color_bgr, self.alpha_maquillaje)
                        elif "bronzer" in self.categoria_actual:
                            self.aplicarContour(frame, face_landmarks, self.color_bgr, self.alpha_maquillaje)    
                    
                    #PARA CUSTOMTKINTER
                    frame_rgb_final = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    imagen_pil = Image.fromarray(frame_rgb_final)

                    if not self.frame_queue.full():
                        self.frame_queue.put_nowait(imagen_pil)
                    
        miWebCam.release()















"""#NO LO BORRES NOOOOOO, POR SI  OCUPO DESPUES
            for face_landmarks in results.multi_face_landmarks:
                for i, landmark in enumerate(face_landmarks.landmark):
                    alto, ancho, _ = frame.shape
                    x = int(landmark.x * ancho)
                    y = int(landmark.y * alto)
                    # Dibuja el número del índice en color verde
                    cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 1)"""
            
