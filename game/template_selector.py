import os
from tkinter import *
from PIL import Image, ImageTk

class TemplateSelector:
    def __init__(self, controller, save_path="template.png"):
        self.controller = controller
        self.save_path = save_path
        self.img_path = self.controller.screenshot()

        self.start_x = self.start_y = self.end_x = self.end_y = 0

        self.window = Tk()
        self.window.title("框選模板區域")

        self.canvas = Canvas(self.window)
        self.canvas.pack()
        self.label = Label(self.window, text="請用滑鼠框選區域")
        self.label.pack()

        self.img = Image.open(self.img_path)
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.config(width=self.img.width, height=self.img.height)
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_img)

        self.rect = None
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.window.mainloop()

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_drag(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_release(self, event):
        self.end_x, self.end_y = event.x, event.y
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        cropped = self.img.crop((x1, y1, x2, y2))
        cropped.save(self.save_path)
        self.label.config(text=f"已儲存模板：{self.save_path}")
        print(f"🖼️ Template saved to {self.save_path}")
