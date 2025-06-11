import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

def cartoonize_image(img, ksize=5, sketch_mode=False):
    num_repetitions, sigma_color, sigma_space, ds_factor = 10, 5, 7, 4
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.medianBlur(img_gray, 7)
    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=ksize)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    if sketch_mode:
        return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    img_small = cv2.resize(img, None, fx=1.0/ds_factor, fy=1.0/ds_factor, interpolation=cv2.INTER_AREA)
    for i in range(num_repetitions):
        img_small = cv2.bilateralFilter(img_small, ksize, sigma_color, sigma_space)
    img_output = cv2.resize(img_small, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_LINEAR)
    dst = cv2.bitwise_and(img_output, img_output, mask=mask)
    return dst

class CartoonApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Cartoonize Webcam")
        self.cap = cv2.VideoCapture(0)
        self.cartoon_mode = False

        self.panel = tk.Label(root)
        self.panel.pack()

        self.btn = tk.Button(root, text="Cartoonize ON", command=self.toggle_cartoon)
        self.btn.pack()

        self.update_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_cartoon(self):
        self.cartoon_mode = not self.cartoon_mode
        self.btn.config(text="Cartoonize OFF" if self.cartoon_mode else "Cartoonize ON")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (480, 360))
            if self.cartoon_mode:
                frame = cartoonize_image(frame, ksize=5, sketch_mode=False)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
        self.root.after(20, self.update_frame)

    def on_close(self):
        self.cap.release()
        self.root.destroy()

root = tk.Tk()
app = CartoonApp(root)
root.mainloop()