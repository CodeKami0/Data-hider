# Final Version of Whispr with Enhanced Attractive UI
from customtkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from stegano import lsb
from datetime import datetime

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

app = CTk()
app.title("Whispr - Hide & Reveal Secrets")
app.geometry("820x660+250+80")
app.resizable(False, False)

filename = None
secret = None
mode = StringVar(value="")

# Functions
def showimage():
    global filename
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select Image File",
        filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("All files", "*.*")]
    )
    if filename:
        try:
            img = Image.open(filename)
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img)
            lbl.image = img
        except Exception as e:
            print("Error:", e)

def Hide():
    global secret
    if filename:
        message = text_box.get("0.0", END).strip()
        if message:
            secret = lsb.hide(filename, message)
            status_label.configure(text="✅ Data hidden successfully!", text_color="green")
        else:
            status_label.configure(text="⚠️ No message to hide.", text_color="red")
    else:
        status_label.configure(text="⚠️ No image selected.", text_color="red")

def Show():
    if filename:
        try:
            revealed = lsb.reveal(filename)
            text_box.delete("0.0", END)
            if revealed:
                text_box.insert(END, revealed)
                status_label.configure(text="✅ Message revealed.", text_color="green")
                save_edit_button.place(x=580, y=550)
            else:
                text_box.insert(END, "No hidden message found!")
                status_label.configure(text="⚠️ No hidden message found.", text_color="orange")
        except Exception as e:
            text_box.insert(END, f"Error: {e}")
    else:
        status_label.configure(text="⚠️ Load an image first.", text_color="red")

def save():
    global secret
    if secret:
        base_name = os.path.splitext(os.path.basename(filename))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"{base_name}_{timestamp}.png"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=default_name,
            title="Save Image With Hidden Data"
        )
        if save_path:
            try:
                secret.save(save_path)
                status_label.configure(text=f"💾 Saved: {os.path.basename(save_path)}", text_color="green")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            status_label.configure(text="❌ Save canceled", text_color="orange")
    else:
        status_label.configure(text="⚠️ No hidden data to save.", text_color="red")

def save_edited_message():
    global secret
    if filename:
        message = text_box.get("0.0", END).strip()
        if message:
            secret = lsb.hide(filename, message)
            save()
        else:
            status_label.configure(text="⚠️ Cannot save empty message.", text_color="red")

def switch_mode(selected_mode):
    mode.set(selected_mode)
    clear_all()
    if selected_mode == "add":
        add_frame.place(x=40, y=100)
        back_button.place(x=700, y=20)
        lbl_frame.place(x=40, y=200)
        textbox_frame.place(x=400, y=200)
    elif selected_mode == "view":
        view_frame.place(x=40, y=100)
        back_button.place(x=700, y=20)
        lbl_frame.place(x=40, y=200)
        textbox_frame.place(x=400, y=200)

def clear_all():
    for widget in [add_frame, view_frame, lbl_frame, textbox_frame, back_button, save_edit_button]:
        widget.place_forget()
    lbl.configure(image="")
    text_box.delete("0.0", END)
    status_label.configure(text="")

def back_to_main():
    clear_all()
    mode.set("")
    mode_frame.place(x=230, y=110)

# --- ENHANCED HOME UI ---
CTkLabel(app, text="Welcome to Whispr", font=("Segoe UI", 28, "bold"), text_color="skyblue").place(x=250, y=20)
CTkLabel(app, text="Your secrets are safe", font=("Segoe UI", 16, "italic"), text_color="gray").place(x=250, y=60)

mode_frame = CTkFrame(app, width=350, height=120, fg_color=("#e0e0e0", "#1a1a1a"), corner_radius=20)
mode_frame.place(x=230, y=110)
CTkButton(mode_frame, text="➕ Add Secret", command=lambda: [mode_frame.place_forget(), switch_mode("add")], width=300, height=40, corner_radius=20, text_color="white", fg_color="#1f2937", hover_color="#2563eb").place(x=25, y=15)
CTkButton(mode_frame, text="👁 Reveal Secret", command=lambda: [mode_frame.place_forget(), switch_mode("view")], width=300, height=40, corner_radius=20, text_color="white", fg_color="#1f2937", hover_color="#9333ea").place(x=25, y=65)


# Footer
CTkLabel(app, text="Built by Rohit", font=("Segoe UI", 12), text_color="gray").place(x=650, y=630)

# Reusable Widgets
back_button = CTkButton(app, text=" Back", command=back_to_main, width=80, corner_radius=15)
save_edit_button = CTkButton(app, text=" Save New", command=save_edited_message, width=140, corner_radius=15)

lbl_frame = CTkFrame(app, width=300, height=280, fg_color=("#f0f0f0", "#2f2f2f"), corner_radius=15)
lbl = CTkLabel(lbl_frame, text="Image Preview", width=250, height=250, corner_radius=10)
lbl.pack(pady=15)

textbox_frame = CTkFrame(app, width=360, height=280, fg_color=("#ffffff", "#2a2a2a"), corner_radius=15)
text_box = CTkTextbox(textbox_frame, width=340, height=250, font=("Consolas", 14), fg_color="#1e1e1e", text_color="white")
text_box.place(x=10, y=10)

add_frame = CTkFrame(app, width=700, height=80, fg_color=("#e0e0e0", "#2a2a2a"), corner_radius=15)
CTkButton(add_frame, text="📂 Open Image", command=showimage, width=160, corner_radius=20).place(x=20, y=20)
CTkButton(add_frame, text="🔐 Hide Data", command=Hide, width=160, corner_radius=20).place(x=200, y=20)
CTkButton(add_frame, text="📎 Save Image", command=save, width=160, corner_radius=20).place(x=380, y=20)

view_frame = CTkFrame(app, width=700, height=80, fg_color=("#e0e0e0", "#2a2a2a"), corner_radius=15)
CTkButton(view_frame, text="📂 Open Image", command=showimage, width=160, corner_radius=20).place(x=20, y=20)
CTkButton(view_frame, text="👁 Show Data", command=Show, width=160, corner_radius=20).place(x=200, y=20)

status_label = CTkLabel(app, text="", font=("Segoe UI", 14))
status_label.place(x=40, y=620)

app.mainloop()