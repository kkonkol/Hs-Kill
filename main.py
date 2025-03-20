import tkinter as tk
import subprocess
import os
import sys

if getattr(sys, 'frozen', False):
    CONFIG_FILE = os.path.join(sys._MEIPASS, "config.txt")
else:
    CONFIG_FILE = "config.txt"

##powered by ja, apka do killowania hs'a

def save_last_rule(rule_name):
    with open(CONFIG_FILE, "w") as file:
        file.write(rule_name)

def load_last_rule():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return file.read().strip()
    return ""

def modify_firewall_rule(rule_name, action):
    if not rule_name:
        status_label.config(text="❌ Podaj nazwę reguły!", fg="red")
        return

    save_last_rule(rule_name)

    command = f'netsh advfirewall firewall set rule name="{rule_name}" new enable={action}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        status_label.config(text=f"✅ Reguła '{rule_name}' {('włączona' if action == 'yes' else 'wyłączona')}", fg="green")
    else:
        status_label.config(text=f"❌ Błąd: Brak uprawnień admina", fg="red")

root = tk.Tk()
root.title("HS Killer")
root.geometry("400x200")

tk.Label(root, text="Nazwa reguły firewalla:").pack(pady=5)

last_rule = load_last_rule()
rule_entry = tk.Entry(root, width=40)
rule_entry.insert(0, last_rule)
rule_entry.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

enable_button = tk.Button(button_frame, text="Włącz", command=lambda: modify_firewall_rule(rule_entry.get(), "yes"), bg="green", fg="white", width=10)
enable_button.pack(side="left", padx=5)

disable_button = tk.Button(button_frame, text="Wyłącz", command=lambda: modify_firewall_rule(rule_entry.get(), "no"), bg="red", fg="white", width=10)
disable_button.pack(side="left", padx=5)

status_label = tk.Label(root, text="🔵 Oczekiwanie na akcję...", fg="blue")
status_label.pack(pady=10)


root.mainloop()
