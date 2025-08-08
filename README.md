# PasMa - Desktop Password Manager

PasMa is a lightweight, Python-based password manager built with Tkinter.  
It allows you to **generate**, **save**, and **retrieve** passwords quickly — all stored locally on your system.



<img width="600" height="600" alt="icon128" src="https://github.com/user-attachments/assets/1528fea9-818b-473e-be00-10e4ed398fda" />





---

## ✨ Features
- 🔑 **Secure password generation** (includes letters, numbers, symbols).
- 💾 **Save credentials locally** in a text file (`passwords_list.txt`).
- 🖥 **Simple and clean interface** using Tkinter.
- 📂 **No external database** — everything is stored locally.

---

## 🖼 Screenshot
<img width="599" height="729" alt="image" src="https://github.com/user-attachments/assets/f82c838b-b517-4df8-a8f7-75e84d878bb7" />


---

## 📦 Requirements
- **Python 3.8+**
- **Tkinter** (comes pre-installed with Python)
- **icon.ico** (optional UI icon)

No additional Python packages are needed for the base version.

---

## 🚀 Installation & Usage
1. **Download the latest release** from the [Releases](../../releases) section.
   - If you download the `.exe` file, no Python installation is required — just run the file.
   - If you download the source code, follow the steps below.
2. Open a terminal and navigate to the `desktop-app/` directory.
3. Run:
```bash
python main.py
```
4. Use the app to generate and store passwords.

---

## 📁 File Structure
```
desktop-app/
│ main.py              # Main Tkinter app script
│ passwords_list.txt   # Saved passwords
│ icon.ico             # Application icon
│ README.md            # This readme
```

---

## ⚠️ Security Note
This is a **basic, educational** password manager.  
- Passwords are stored in **plain text** by default in `passwords_list.txt`.
- For production use, add **AES encryption** or integrate with secure storage (like `keyring`).

---

## 📜 License
This project is licensed under the MIT License.
