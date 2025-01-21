from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb  # pip install stegano

# Initialize the main application window
root = Tk()
root.title("Steganography - Text Hider in Image")
root.geometry("700x500+250+180")
root.resizable(False, False)
root.configure(bg="#2f4155")

# Function to open and display an image
def showimage():
    global filename
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(), title="Select Image File",
        filetype=(("PNG file", "*.png"), ("JPG File", "*.jpg"), ("All file", "*.*"))
    )

    if filename:
        try:
            img = Image.open(filename)  # Open the selected image
            img = img.resize((250, 250), Image.Resampling.LANCZOS)  # Resize for display
            img = ImageTk.PhotoImage(img)  # Convert to PhotoImage
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img  # Keep a reference to prevent garbage collection
        except Exception as e:
            print(f"Error loading image: {e}")


# Function to hide text in an image
def Hide():
    global secret
    if 'filename' in globals():
        message = text1.get(1.0, END).strip()
        if message:
            secret = lsb.hide(filename, message)
            Label(frame3, text="Data Hidden Successfully!", bg="#2f4155", fg="yellow").place(x=20, y=70)
        else:
            Label(frame3, text="No message to hide!", bg="#2f4155", fg="red").place(x=20, y=70)
    else:
        Label(frame3, text="No image selected!", bg="#2f4155", fg="red").place(x=20, y=70)

# Function to reveal hidden text from an image
def Show():
    if 'filename' in globals():
        try:
            clear_message = lsb.reveal(filename)
            text1.delete(1.0, END)
            text1.insert(END, clear_message if clear_message else "No hidden message found!")
        except Exception as e:
            text1.delete(1.0, END)
            text1.insert(END, f"Error: {str(e)}")
    else:
        text1.delete(1.0, END)
        text1.insert(END, "No image selected!")

# Function to save the image with hidden text
def save():
    if 'secret' in globals():
        secret.save("hidden.png")
        Label(frame3, text="Image Saved as hidden.png!", bg="#2f4155", fg="yellow").place(x=20, y=70)
    else:
        Label(frame3, text="No hidden data to save!", bg="#2f4155", fg="red").place(x=20, y=70)

# Load application icon
icon_path = os.path.join(os.getcwd(), "images", "person.jpg")
if os.path.exists(icon_path):
    image_icon = PhotoImage(file=icon_path)
    root.iconphoto(False, image_icon)
else:
    print(f"Warning: Icon file '{icon_path}' not found.")

# Load application logo
logo_path = os.path.join(os.getcwd(), "images", "logo.png")
if os.path.exists(logo_path):
    logo = PhotoImage(file=logo_path)
    Label(root, image=logo, bg="#2f4155").place(x=10, y=0)
else:
    print(f"Warning: Logo file '{logo_path}' not found.")


Label(root, text="CYBER SCIENCE", bg="#2f4155", fg="white", font="arial 25 bold").place(x=100, y=20)

# First frame for displaying the selected image
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=40, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second frame for text input/output
frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="Robote 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third frame for image operations
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Picture, Image", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Fourth frame for text hiding/revealing operations
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Label(frame4, text="Picture, Image", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Start the main event loop
root.mainloop()
