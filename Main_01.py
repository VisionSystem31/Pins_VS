import tkinter as tk
from PIL import Image, ImageTk 
import cv2
import imutils
import numpy as np
from datetime import datetime
from ultralytics import YOLO
import subprocess

def visualizar():
    global inicio, cap, frame, model, class_names, texto1, texto3, BoxShadow_id, counter, vector

    if inicio == 1:
        model = YOLO("/home/jetson/Documents/AI/Pins_VS/Dimples_S01.pt")
        cap = cv2.VideoCapture(0)
        # cap.set(4, 480) #Alto
        # cap.set(3, 640) #Ancho
        class_names = ["Dimple"]
        inicio = 0
        counter = 1
        vector = []
    else:
        pantalla.delete(frame)
        pantalla.delete(texto1)
        pantalla.delete(texto3)
        pantalla.delete(BoxShadow_id)

    # if counter < 8:
    #     BoxShadow_id = pantalla.create_image(155, 75, anchor=tk.NW, image=BoxShadow)
    #     Close_Button.configure(bg = "#FFFFFF")
    #     pantalla.configure(bg = "#FFFFFF")
    #     texto1 = pantalla.create_text(500, 55, text="Dimples Vision System", font=("Helvetica", 30, "bold"), fill="black")
    #     texto3 = pantalla.create_text(500, 640, text=f"Waiting for the Dimple", font=("Helvetica", 30, "bold"), fill="black")

    # elif counter < 10:
    #     BoxShadow_id = pantalla.create_image(155, 75, anchor=tk.NW, image=BoxShadow)
    #     Close_Button.configure(bg = "#008000")
    #     pantalla.configure(bg = "#008000")
    #     texto1 = pantalla.create_text(500, 55, text="Dimples Vision System", font=("Helvetica", 30, "bold"), fill="white")
    #     texto3 = pantalla.create_text(500, 640, text=f"Dimple Found", font=("Helvetica", 30, "bold"), fill="white")

    # else:
    #     Close_Button.configure(bg = "#FF0035")
    #     pantalla.configure(bg = "#FF0035")
    #     BoxShadow_id = pantalla.create_image(155, 75, anchor=tk.NW, image=BoxShadow)
    #     texto1 = pantalla.create_text(500, 55, text="Dimples Vision System", font=("Helvetica", 30, "bold"), fill="white")
    #     texto3 = pantalla.create_text(500, 640, text=f"Waiting for detection...", font=("Helvetica", 30, "bold"), fill="white")

    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            results = model.predict(frame, verbose=True, agnostic_nms=True, conf = 0.50, imgsz = 640)
            height, width, _ = frame.shape

            if results is not None:
                for result in results:
                    if result.boxes:
                        for box in result.boxes:
                            class_id = int(box.cls[0].item())
                            cords = box.xyxy[0].tolist()
                            x1, y1, x2, y2 = map(int, cords)

                            if class_id == 0: 
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                                cv2.putText(frame, f"{class_names[0]}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
                                vector.append(class_id)
                    else:
                        vector = [] 
            if len(vector) == 5:
                vector = []
                BoxShadow_id = pantalla.create_image(155, 75, anchor=tk.NW, image=BoxShadow)
                Close_Button.configure(bg = "#008000")
                pantalla.configure(bg = "#008000")
                texto1 = pantalla.create_text(500, 55, text="Dimples Vision System", font=("Helvetica", 30, "bold"), fill="white")
                texto3 = pantalla.create_text(500, 640, text=f"Dimple Found", font=("Helvetica", 30, "bold"), fill="white")
            else:
                BoxShadow_id = pantalla.create_image(155, 75, anchor=tk.NW, image=BoxShadow)
                Close_Button.configure(bg = "#FFFFFF")
                pantalla.configure(bg = "#FFFFFF")
                texto1 = pantalla.create_text(500, 55, text="Dimples Vision System", font=("Helvetica", 30, "bold"), fill="black")
                texto3 = pantalla.create_text(500, 640, text=f"Waiting for the Dimple", font=("Helvetica", 30, "bold"), fill="black")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=640, height=480)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            pantalla.after(10, visualizar)
        else:
            cap.release()

def turn_off_action():
    root.destroy()

root = tk.Tk()
root.title("Pins Vision System")

root.attributes('-fullscreen', True)

pantalla = tk.Canvas(root, width=1000, height=700, bg="#FFFFFF")
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
