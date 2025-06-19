import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import os
import datetime

# Load known face encodings
def load_known_faces(folder='known_faces'):
    encodings = []
    names = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        image = face_recognition.load_image_file(path)
        face_encs = face_recognition.face_encodings(image)
        if face_encs:
            encodings.append(face_encs[0])
            names.append(os.path.splitext(filename)[0])
    return encodings, names

# Log results to logs.txt
def log_result(name):
    with open("logs.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - {name}\n")

# Run authentication
def authenticate():
    known_encodings, known_names = load_known_faces()

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Error", "Failed to capture image from webcam.")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encs = face_recognition.face_encodings(rgb_frame)

    name = "Not Genuine"

    if face_encs:
        face_enc = face_encs[0]
        matches = face_recognition.compare_faces(known_encodings, face_enc)
        if True in matches:
            index = matches.index(True)
            name = f"Genuine: {known_names[index]}"

    log_result(name)
    messagebox.showinfo("Result", name)

    # Show captured photo
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img.thumbnail((400, 300))
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img

# GUI setup
root = tk.Tk()
root.title("Face Authentication System")

tk.Label(root, text="Click the button to authenticate via camera").pack(pady=10)
tk.Button(root, text="Authenticate", command=authenticate, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

root.mainloop()
 