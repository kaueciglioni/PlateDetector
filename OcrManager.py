import cv2
import time
import re
from ultralytics import YOLO
from paddleocr import PaddleOCR
import Logger as Log
import numpy as np

# -------- OCR Manager --------
class OcrManager():
    def __init__(self, p_confidence):
        try:
            self.model = PaddleOCR(use_angle_cls=True, lang='pt')
            self.Confidence = p_confidence
            self.rePlatePatern = r'\b[A-Z0]{3}-?\d[A-Z0-9]\d{2}\b'
            self.reTagCodePatern = r'\b[A-Z]{3}\d{3}[A-Z0-9]{4}\b'
            self.reTagProductCodePatern = r'\b[0-9Oo]{11}\b'
        except Exception as e:
            Log.error("OcrManager", "__init__", str(e))

    def PredictPlate(self, p_frame):
        try:
            result = self.model.ocr(p_frame)
            for Line in result[0]:
                DetectedText = Line[1][0]
                Confidence = Line[1][1]
                if Confidence >= self.Confidence:
                    Matches = re.findall(self.rePlatePatern, DetectedText, re.IGNORECASE)
                    if Matches:
                        return Matches[0]
            return None
        except Exception as e:
            Log.error("OcrManager", "PredictPlate", str(e))

# -------- Inicialização --------
CONFIDENCE = 0.5
ocr = OcrManager(p_confidence=CONFIDENCE)
model = YOLO('Plate.pt')  # Substitua pelo caminho do seu modelo

operation_active = False
plate_text_last = None

# -------- Leitura do vídeo --------
cap = cv2.VideoCapture("20250701_192617000_iOS.mp4")
if not cap.isOpened():
    raise Exception("Erro ao abrir o vídeo.")

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
activation_line_y = int(frame_height * 0.25)

last_y_center = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    plate_detected_this_frame = False
    plate_text = None  # Reset a cada frame

    for result in results:
        for box in result.boxes:
            conf = float(box.conf)
            if conf < 0.5:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)

            # Verifica se a placa está se movendo verticalmente
            if last_y_center is not None:
                print(f"Last Y center: {last_y_center}, Current Y center: {y_center}, Line Y: {activation_line_y}")

                Starter = last_y_center > activation_line_y and y_center <= activation_line_y
                Ended = last_y_center < activation_line_y and y_center >= activation_line_y

                # INÍCIO → cruzamento de baixo para cima
                if  Starter:
                    crop = frame[y1:y2, x1:x2]
                    PlateText = ocr.PredictPlate(crop)
                    if PlateText and not operation_active:
                        operation_active = True
                        plate_text_last = PlateText
                        plate_detected_this_frame = True
                        print(f">> Operation STARTED — Plate: {PlateText}")

                # FIM → cruzamento de cima para baixo
                elif Ended:
                    crop = frame[y1:y2, x1:x2]
                    PlateText = ocr.PredictPlate(crop)
                    if PlateText and operation_active:
                        operation_active = False
                        print("<< Operation ENDED")

            # Atualiza posição do centro da placa
            last_y_center = y_center

            # Desenha bounding box e texto
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if plate_text_last:
                cv2.putText(frame, plate_text_last, (x1, y1 - 10), cv2.FONT_HERqSHEY_SIMPLEX,
                            0.9, (0, 255, 0), 2, cv2.LINE_AA)
              # processa apenas a primeira placa válida

    # Desenha a linha de ativação (em azul)
    cv2.line(frame, (0, activation_line_y), (frame.shape[1], activation_line_y), (255, 0, 0), 2)

    # Mostrar o frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
