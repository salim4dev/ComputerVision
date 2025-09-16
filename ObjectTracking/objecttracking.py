import cv2

# ---- 1. Snapshot et sélection ROI ----
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Corriger orientation (0 = flip vertical, 1 = flip horizontal, -1 = flip les deux)
frame = cv2.flip(frame, -1)  # Ici on met -1 pour effet miroir horizontal et vertical

bbox = cv2.selectROI("Snapshot - Select ROI", frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()
cap.release()

# ---- 2. Relancer flux ----
cap = cv2.VideoCapture(0)

# Choix du tracker (MOSSE = rapide, KCF/CSRT = plus précis mais lourds)
# tracker = cv2.legacy.TrackerKCF_create()
# tracker = cv2.legacy.TrackerCSRT_create()
tracker = cv2.legacy.TrackerMOSSE_create()  # ⚡ recommandé sur Raspberry Pi

tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Corriger orientation (0 = flip vertical, 1 = flip horizontal, -1 = flip les deux)
    frame = cv2.flip(frame, -1)  # Ici on met -1 pour effet miroir horizontal et vertical

    success, box = tracker.update(frame)

    if success:
        x, y, w, h = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking...", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Lost!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
