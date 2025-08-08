import os
import sys
import hashlib
import random
from tkinter import *
from tkinter import messagebox, simpledialog
import pyperclip

BG_COLOR = "#23272a"
FIELD_BG = "#2c2f33"
FG_COLOR = "#ffffff"
BTN_BG = "#2c2f33"
BTN_FG = "#ffffff"
ACTIVE_BTN_BG = "#3a3e43"
ACTIVE_BTN_FG = "#ffffff"
LABEL_COLOR = "#a7acb2"

APP_NAME = "PasMa"
APPDATA_PATH = os.getenv('APPDATA')
APP_DIR = os.path.join(APPDATA_PATH, APP_NAME)
os.makedirs(APP_DIR, exist_ok=True)

MASTER_PASSWORD_FILE = os.path.join(APP_DIR, "master_password.txt")
PASSWORDS_FILE = os.path.join(APP_DIR, "passwords_list.txt")
authenticated = False

def get_resource_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_master_password(password):
    with open(MASTER_PASSWORD_FILE, "w") as f:
        f.write(hash_password(password))

def load_master_password_hash():
    if not os.path.exists(MASTER_PASSWORD_FILE):
        return None
    with open(MASTER_PASSWORD_FILE, "r") as f:
        return f.read().strip()

def prompt_set_master_password():
    while True:
        password1 = simpledialog.askstring("Set Master Password", "Create a new master password:", show='*')
        if password1 is None:
            return False
        password2 = simpledialog.askstring("Set Master Password", "Confirm the new master password:", show='*')
        if password2 is None:
            return False
        if password1 == password2 and password1.strip():
            save_master_password(password1)
            messagebox.showinfo("Success", "Master password set successfully.")
            return True
        else:
            messagebox.showerror("Error", "Passwords do not match or empty. Please try again.")

def prompt_login():
    saved_hash = load_master_password_hash()
    if saved_hash is None:
        return prompt_set_master_password()
    for _ in range(3):
        password = simpledialog.askstring("Login", "Enter master password:", show='*')
        if password is None:
            return False
        if hash_password(password) == saved_hash:
            return True
        else:
            messagebox.showerror("Error", "Incorrect password. Try again.")
    return False

def authenticate_user():
    global authenticated
    if authenticated:
        return True
    success = prompt_login()
    if success:
        authenticated = True
    return success

def reset_master_password():
    global authenticated
    if not authenticate_user():
        messagebox.showinfo("Access Denied", "Authentication failed.")
        return
    current_password = simpledialog.askstring("Reset Password", "Enter current master password again:", show='*')
    if current_password is None:
        return
    if hash_password(current_password) != load_master_password_hash():
        messagebox.showerror("Error", "Incorrect master password.")
        return
    confirm = messagebox.askyesno(
        "Confirm Reset",
        "Resetting the master password will DELETE all saved passwords.\nAre you sure you want to continue?"
    )
    if not confirm:
        return
    try:
        if os.path.exists(MASTER_PASSWORD_FILE):
            os.remove(MASTER_PASSWORD_FILE)
        if os.path.exists(PASSWORDS_FILE):
            os.remove(PASSWORDS_FILE)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to reset files: {e}")
        return
    authenticated = False
    messagebox.showinfo("Reset Successful", "Please set a new master password.")
    if not prompt_set_master_password():
        messagebox.showerror("Error", "Master password not set.")
        return
    if prompt_login():
        authenticated = True
        messagebox.showinfo("Success", "Master password reset and login successful.")
    else:
        messagebox.showerror("Error", "Login failed after reset.")

def generate_password():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    password_chars = (
        random.choices(letters, k=6) +
        random.choices(numbers, k=3) +
        random.choices(symbols, k=3)
    )
    random.shuffle(password_chars)
    password = "".join(password_chars)
    pyperclip.copy(password)
    pass_input.delete(0, END)
    pass_input.insert(0, password)

def save_pass():
    website_input = web_input.get()
    email_input = em_input.get()
    password_input = pass_input.get()
    if len(website_input) == 0 or len(password_input) == 0:
        messagebox.showwarning(title="Oops!", message="Don't leave the website or password empty!")
        return
    is_ok = messagebox.askokcancel(
        title=website_input,
        message=f"These are the details entered:\nEmail: {email_input}\nPassword: {password_input}\nSave?"
    )
    if is_ok:
        with open(PASSWORDS_FILE, "a") as file:
            file.write(f"Website: {website_input}  |  Email: {email_input}  |  Password: {password_input}\n")
        web_input.delete(0, END)
        pass_input.delete(0, END)

def view_passwords():
    if not authenticate_user():
        return
    view_win = Toplevel(window)
    view_win.title("Saved Passwords")
    view_win.config(bg=BG_COLOR, padx=20, pady=20)
    text_widget = Text(view_win, width=120, height=20, bg=FIELD_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
    text_widget.pack()
    try:
        with open(PASSWORDS_FILE, "r") as file:
            passwords = file.read()
            text_widget.insert(END, passwords)
    except FileNotFoundError:
        text_widget.insert(END, "No saved passwords found.")
    text_widget.config(state='disabled')

window = Tk()
window.title("PasMa")
try:
    window.iconbitmap(get_resource_path("icon.ico"))
except Exception:
    pass
window.config(bg=BG_COLOR, padx=50, pady=50)

canvas = Canvas(height=200, width=200, bg=BG_COLOR, highlightthickness=0)
try:
    logo_img = PhotoImage(file=get_resource_path("logo.png"))
    canvas.create_image(100, 100, image=logo_img)
except Exception:
    canvas.create_text(100, 100, text="PasMa", fill=FG_COLOR, font=("Helvetica", 24, "bold"))
canvas.grid(row=0, column=0, columnspan=3, pady=10)

Label(text="Website:", bg=BG_COLOR, fg=LABEL_COLOR).grid(row=1, column=0, pady=5, sticky="w")
Label(text="Email/Username:", bg=BG_COLOR, fg=LABEL_COLOR).grid(row=2, column=0, pady=5, sticky="w")
Label(text="Password:", bg=BG_COLOR, fg=LABEL_COLOR).grid(row=3, column=0, pady=5, sticky="w")

web_input = Entry(width=35, bg=FIELD_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
web_input.grid(row=1, column=1, columnspan=2, pady=5)
web_input.focus()

em_input = Entry(width=35, bg=FIELD_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
em_input.grid(row=2, column=1, columnspan=2, pady=5)
em_input.insert(0, "example@gmail.com")

pass_input = Entry(width=21, bg=FIELD_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
pass_input.grid(row=3, column=1, pady=5)

button_font = ("Helvetica", 10, "bold")

Button(
    text="Generate", command=generate_password,
    width=15,
    bg=BTN_BG,
    fg=BTN_FG,
    activebackground=ACTIVE_BTN_BG,
    activeforeground=ACTIVE_BTN_FG,
    relief="ridge",
    font=button_font
).grid(row=3, column=2, padx=5, pady=3)

Button(
    text="Add", command=save_pass,
    width=35,
    bg=BTN_BG,
    fg=BTN_FG,
    activebackground=ACTIVE_BTN_BG,
    activeforeground=ACTIVE_BTN_FG,
    relief="ridge",
    font=button_font
).grid(row=4, column=1, columnspan=2, pady=10)

Button(
    text="View Passwords", command=view_passwords,
    width=35,
    bg=BTN_BG,
    fg=BTN_FG,
    activebackground=ACTIVE_BTN_BG,
    activeforeground=ACTIVE_BTN_FG,
    relief="ridge",
    font=button_font
).grid(row=5, column=1, columnspan=2, pady=10)

Button(
    text="Reset Password", command=reset_master_password,
    width=35,
    bg=BTN_BG,
    fg=BTN_FG,
    activebackground=ACTIVE_BTN_BG,
    activeforeground=ACTIVE_BTN_FG,
    relief="ridge",
    font=button_font
).grid(row=6, column=1, columnspan=2, pady=10)

window.mainloop()
