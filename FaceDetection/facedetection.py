import cv2

# Charger le classificateur pré-entraîné pour le visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Démarrer la capture webcam
cap = cv2.VideoCapture(0)  # 0 pour la webcam par défaut

while True:
    # Lire l'image depuis la webcam
    ret, frame = cap.read()
    if not ret:
        print("Impossible de lire la webcam")
        break
    # Corriger orientation (0 = flip vertical, 1 = flip horizontal, -1 = flip les deux)
    frame = cv2.flip(frame, -1)  # Ici on met -1 pour effet miroir horizontal et vertical

    # Convertir l'image en niveaux de gris (nécessaire pour le détecteur Haar)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection des visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Dessiner un rectangle autour des visages détectés
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Afficher le flux en temps réel
    cv2.imshow('Detection Visage', frame)

    # Sortir avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()

