import os
from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from tkinter.filedialog import askopenfilename

import cv2
from PIL import ImageTk, Image
from unidecode import unidecode

import database
import finger
import minucje

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def link(id):
    if id == 1:
        global filename1
        filename1 = askopenfilename()
        update_image(filename1, image_2)
        Clear()
    elif id == 2:
        global filename2
        filename2 = askopenfilename()
        finger.finger(filename1, filename2, 1)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Identyfikacja")
window.geometry("606x751")
window.configure(bg="#0070D8")

canvas = Canvas(
    window,
    bg="#0070D8",
    height=751,
    width=606,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    600.0,
    464.0,
    image=image_image_1,
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: minuc(),
    relief="flat"
)
button_1.place(
    x=380.0,
    y=235.0,
    width=193.0,
    height=34.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: DBase(),
    relief="flat"
)
button_2.place(
    x=380.0,
    y=308.0,
    width=193.0,
    height=34.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: link(2),
    relief="flat"
)
button_3.place(
    x=380.0,
    y=381.0,
    width=193.0,
    height=34.0
)
button_3.pack_forget()
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: baza(),
    relief="flat",
    state="normal"
)
button_4.place(
    x=380.0,
    y=604.0,
    width=193.0,
    height=34.0
)
nameToSave = Entry(canvas)
nameToSave.place(
    x=381.0,
    y=560.0,
    width=193.0,
    height=28.0,
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: link(1),
    relief="flat"
)
button_5.place(
    x=128.0,
    y=102.0,
    width=110.0,
    height=28.0
)

canvas.create_text(
    141.0,
    23.0,
    anchor="nw",
    text="IDENTYFIKACJA ODCISKU PALCA",
    fill="#FFFFFF",
    font=("Gotu Regular", 20 * -1)
)

matched = canvas.create_text(
    23.0,
    688.0,
    anchor="nw",
    text="",
    fill="#FFFFFF",
    font=("Inter", 17 * -1)
)

score = canvas.create_text(
    154.0,
    688.0,
    anchor="nw",
    text="",
    fill="#FFFFFF",
    font=("Inter", 17 * -1)
)

err = canvas.create_text(
    380.0,
    650.0,
    anchor="nw",
    text="",
    fill="#00FF00",
    font=("Inter", 15 * -1)
)

nameData = canvas.create_text(
    381.0,
    531.0,
    anchor="nw",
    text="Podaj Imię i Nazwisko",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    183.0,
    398.0,
    image=image_image_2
)

name = canvas.create_text(
    23.0,
    658.0,
    anchor="nw",
    text="",
    fill="#FFFFFF",
    font=("Inter", 17 * -1)
)


def update_image(path, button):
    image = Image.open(path)
    image = image.resize((320, 480), Image.LANCZOS)
    image = ImageTk.PhotoImage(image)
    canvas.itemconfig(button, image=image)
    label = Label(window, image=image)
    label.image = image


def minuc():
    res = minucje.minucje(filename1)
    image = Image.fromarray(res)
    image = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_2, image=image)
    label = Label(window, image=image)
    label.image = image

def DBase():
    date = database.inDatabase(filename1)
    canvas.itemconfig(name, text=(date[0]))
    canvas.itemconfig(score, text=round(date[1]))
    canvas.itemconfig(matched, text="Dopasowanie")


def Clear():
    canvas.itemconfig(name, text="")
    canvas.itemconfig(score, text="")
    canvas.itemconfig(matched, text="")
    canvas.itemconfig(err, text="")


def baza():
    text = nameToSave.get()
    have = 0
    if text == "":
        canvas.itemconfig(err, text="Puste pole", fill="#FF0000")
    else:
        text = unidecode(text)
        names = (os.listdir('finger'))
        for x in names:
            if x == text:
                have = 1
                break
        if have == 0:
            os.mkdir('finger/' + text)
        img = cv2.imread(filename1)
        os.chdir('finger/' + text)
        amount = os.listdir()
        filename = 'odcisk' + str(len(amount) + 1) + '.jpg'
        cv2.imwrite(filename, img)
        os.chdir("..")
        os.chdir("..")
        canvas.itemconfig(err, text="Dodano do bazy!", fill="#00FF00")


window.resizable(False, False)
window.mainloop()
