import hashlib
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# Colors
DARK_BG = "#1a1a1a"
LIGHT_BG = "#2d2d2d"
ACCENT = "#5865F2"
TEXT_WHITE = "#ffffff"

def open_discord():
    webbrowser.open("https://discord.gg/y92sn3EsWR")

def check_password():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password!")
        return
    
    # Calculate SHA-1 hash
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    
    try:
        # Query HaveIBeenPwned API
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code != 200:
            messagebox.showerror("Error", "Connection to security service failed")
            return
        
        # Buscar coincidencias
        found = False
        for line in response.text.splitlines():
            if line.split(":")[0] == suffix:
                count = int(line.split(":")[1])
                messagebox.showwarning(
                    "Password Compromised!",
                    f"This password appears in {count} known data breaches.\n\n"
                    "DO NOT use it for any online service!\n\n"
                    "Join our Discord for security tips: discord.gg/MSukhfr6k3"
                )
                found = True
                break
        
        if not found:
            messagebox.showinfo("Secure Password", "✅ Password not found in known breaches")
            
    except Exception as e:
        messagebox.showerror("Error", f"Connection error: {str(e)}")

# Configuración de la GUI
root = tk.Tk()
root.title("PassGuard v1.0")
root.geometry("400x220")
root.configure(bg=DARK_BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background=DARK_BG)
style.configure("TLabel", background=DARK_BG, foreground=TEXT_WHITE)
style.configure("TEntry", fieldbackground=LIGHT_BG, foreground=TEXT_WHITE)
style.configure("TButton", background=ACCENT, foreground=TEXT_WHITE)

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(main_frame, text="🔒 Check Password Security:").pack(pady=5)
entry_password = ttk.Entry(main_frame, show="•", width=30)
entry_password.pack(pady=5)

btn_frame = ttk.Frame(main_frame)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Check Security", command=check_password).pack(side=tk.LEFT, padx=5)
ttk.Button(btn_frame, text="Join Discord", command=open_discord).pack(side=tk.LEFT, padx=5)

footer = ttk.Label(main_frame, text="Need help? Join our security community!", font=("Arial", 8))
footer.pack(side=tk.BOTTOM, pady=5)

root.mainloop()