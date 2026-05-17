import customtkinter as ctk
from tkinter import messagebox
import os

# APP SETTINGS
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# MAIN WINDOW
root = ctk.CTk()
root.geometry("500x600")
root.title("Admin Login")

# LOGIN FUNCTION
def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "harshii" and password == "harshitha1980":

        messagebox.showinfo(
            "Success",
            "Welcome Harshii"
        )

        root.destroy()

        os.system("python admin_dashboard.py")

    else:

        messagebox.showerror(
            "Error",
            "Wrong Username or Password"
        )

# TITLE
title = ctk.CTkLabel(
    root,
    text="ADMIN LOGIN",
    font=("Arial", 32, "bold")
)

title.pack(pady=40)

# FRAME
frame = ctk.CTkFrame(root)
frame.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

# USERNAME
username_label = ctk.CTkLabel(
    frame,
    text="Username"
)

username_label.pack(pady=10)

username_entry = ctk.CTkEntry(
    frame,
    width=300,
    height=40
)

username_entry.pack(pady=10)

# PASSWORD
password_label = ctk.CTkLabel(
    frame,
    text="Password"
)

password_label.pack(pady=10)

password_entry = ctk.CTkEntry(
    frame,
    width=300,
    height=40,
    show="*"
)

password_entry.pack(pady=10)

# LOGIN BUTTON
login_button = ctk.CTkButton(
    frame,
    text="LOGIN",
    width=300,
    height=45,
    command=login
)

login_button.pack(pady=40)

# RUN APP
root.mainloop()