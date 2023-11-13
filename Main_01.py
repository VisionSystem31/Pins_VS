import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import cv2
import imutils
import numpy as np
from datetime import datetime
from ultralytics import YOLO
import subprocess
import Jetson.GPIO as GPIO
import os 

Salida = 11
energy_cut = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(energy_cut, GPIO.IN)

GPIO.setup(Salida, GPIO.OUT)
GPIO.output(Salida, True)

def visualizar():
    global inicio, cap, frame, model, class_names, texto1, BoxShadow_id, counter, vector

    if inicio == 1:
        model = YOLO("/home/jetson/Documents/AI/Pins_VS/Dimples_S02.pt")
        cap = cv2.VideoCapture(0)
        class_names = ["Dimple Found"]
        inicio = 0
        counter = 1
        vector = []
        BoxShadow_id = pantalla.create_image(155, 75, anchor=tk.NW, image=BoxShadow)
    else:
        pantalla.delete(frame)
        pantalla.delete(texto1)
    
    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            results = model.predict(frame, verbose=False, agnostic_nms=True, conf = 0.50, imgsz = 416, device = 0)
            height, width, _ = frame.shape

            if results is not None:
                for result in results:
                    if result.boxes:
                        for box in result.boxes:
                            class_id = int(box.cls[0].item())
                            cords = box.xyxy[0].tolist()
                            x1, y1, x2, y2 = map(int, cords)

                            if class_id == 0: 
                                vector.append(class_id)
                    else:
                        vector = [] 
            if len(vector) >= 7:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                cv2.putText(frame, f"{class_names[0]}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
                GPIO.output(Salida, False)
                Close_Button.configure(bg = "#008000")
                pantalla.configure(bg = "#008000")
                texto1 = pantalla.create_text(500, 55, text="Dimples Vision System", font=("Helvetica", 30, "bold"), fill="white")
            else:
                GPIO.output(Salida, True)
                Close_Button.configure(bg = "#FFFFFF")
                pantalla.configure(bg = "#FFFFFF")
                texto1 = pantalla.create_text(500, 55, text="Dimples Vision System", font=("Helvetica", 30, "bold"), fill="black")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=640, height=480)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img

            if GPIO.input(energy_cut):
                os.system("sudo shutdown -h now")
            
            pantalla.after(10, visualizar)
        else:
            cap.release()

def turn_off_action():
    result = messagebox.askquestion("Confirmar apagado", "Seguro quiere apagar el sistema de vision?", icon='warning')
    if result == 'yes':
        os.system("sudo shutdown -h now")
        root.destroy()

root = tk.Tk()
root.title("Dimples Vision System")

root.attributes('-fullscreen', True)

pantalla = tk.Canvas(root, width=1200, height=700, bg="#FFFFFF")
pantalla.pack()

#Backgrounds
BoxShadow = tk.PhotoImage(file="/home/jetson/Documents/AI/Pins_VS/IMG/BoxShadow.png")

#Boton de cerrado
Close = tk.PhotoImage(file="/home/jetson/Documents/AI/Pins_VS/IMG/shutdown.png")
Close_Button = tk.Button(pantalla, image=Close, bg="#FFFFFF", command=turn_off_action, borderwidth=0, relief="flat")
Close_Button.place(x = 900, y = 21)

lblVideo = tk.Label(pantalla)
lblVideo.configure(borderwidth=0)
lblVideo.place(x = 180, y = 100)
inicio = 1

visualizar()

#FFFFFF -> Blanco
#FF0035 -> Rojo
#008000 -> verde

root.mainloop()
