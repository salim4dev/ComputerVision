
import cv2
import numpy as np

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

# Couleurs et plages HSV
couleurs = {
    "Rouge": [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])],
    "Vert": [([36, 50, 70], [89, 255, 255])],
    "Bleu": [([90, 60, 0], [121, 255, 255])],
    "Jaune": [([20, 100, 100], [30, 255, 255])],
    "Orange": [([10, 100, 20], [20, 255, 255])],
    "Violet": [([130, 50, 50], [160, 255, 255])],
    "Cyan": [([85, 50, 50], [95, 255, 255])],
    "Rose": [([145, 50, 50], [170, 255, 255])]
}

# Couleurs BGR pour rectangles
couleurs_bgr = {
    "Rouge": (0, 0, 255),
    "Vert": (0, 255, 0),
    "Bleu": (255, 0, 0),
    "Jaune": (0, 255, 255),
    "Orange": (0, 165, 255),
    "Violet": (255, 0, 255),
    "Cyan": (255, 255, 0),
    "Rose": (203, 192, 255)
}

# Boucle principale
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Effet miroir
    frame = cv2.flip(frame, 1)

    # Conversion HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Détection
    for nom, plages in couleurs.items():
        mask_total = None
        for lower, upper in plages:
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

        contours, _ = cv2.findContours(mask_total, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), couleurs_bgr[nom], 2)
                cv2.putText(frame, nom, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, couleurs_bgr[nom], 2)

    # Affichage
    cv2.imshow("Détection Couleurs Complète", frame)

    # Quitter avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
