from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from tkinter import *
from PIL import Image, ImageTk


def refreshScreen(svg):
    drawing = svg2rlg(svg)
    renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
    img = Image.open('temp.png')
    pimg = ImageTk.PhotoImage(img)
    size = img.size

    frame = Canvas(tk, width=size[0], height=size[1])
    frame.pack()
    frame.create_image(0, 0, anchor='nw', image=pimg)


tk = Tk()
tk.mainloop()
