import cv2
import numpy as np
import mediapipe as mp
from landmarks import FACE_ZONES
#FORMULA GENERAL Resultado(x,y) = Original(x,y) \cdot (1 - \alpha_{mask}) + Maquillaje(x,y) \cdot \alpha_{mask}$

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# NO OLVIDAR
miWebCam = cv2.VideoCapture(0)



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
    mask = cv2.GaussianBlur(mask, (21, 21), 0) #impar para que no se vea como payaso

    alpha_mask = (mask / 255.0) * alpha
    alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
    color_layer = np.full((alto, ancho, 3), color_bgr, dtype=np.uint8)
    frame[:] = (frame * (1 - alpha_mask_3c) + color_layer * alpha_mask_3c).astype(np.uint8)




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
    mask = cv2.GaussianBlur(mask, (51, 51), 0) #impar para que no se vea como payaso
    alpha_mask = (mask / 255.0) * alpha
    alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
    color_layer = np.full((alto, ancho, 3), color_bgr, dtype=np.uint8)
    frame[:] = (frame * (1 - alpha_mask_3c) + color_layer * alpha_mask_3c).astype(np.uint8)


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
    mask = cv2.GaussianBlur(mask, (41, 41), 0) #impar para que no se vea como payaso
    alpha_mask = (mask / 255.0) * alpha
    alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
    color_layer = np.full((alto, ancho, 3), color_bgr, dtype=np.uint8)
    frame[:] = (frame * (1 - alpha_mask_3c) + color_layer * alpha_mask_3c).astype(np.uint8)



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


with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
        
    while miWebCam.isOpened():
        ret, frame = miWebCam.read()
        
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                aplicarLabial(frame, face_landmarks, color_bgr=(50, 50, 200), alpha=0.3)
                aplicarRubor(frame, face_landmarks, color_bgr=(50, 50, 200), alpha=0.3)
                aplicarSombra(frame, face_landmarks, color_bgr=(50, 50, 200), alpha=0.3)
                aplicarContour(frame, face_landmarks, color_bgr=(30, 80, 130), alpha=0.4)
                
            """NO LO BORRES NOOOOOO, POR SI  OCUPO DESPUES
            for face_landmarks in results.multi_face_landmarks:
                for i, landmark in enumerate(face_landmarks.landmark):
                    alto, ancho, _ = frame.shape
                    x = int(landmark.x * ancho)
                    y = int(landmark.y * alto)
                    # Dibuja el número del índice en color verde
                    cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 1)
        cv2.imshow("Tester OMCA", frame)"""
            
        cv2.imshow("Tester OMCA", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

miWebCam.release()
cv2.destroyAllWindows()