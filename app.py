import tkinter as tk
from datetime import datetime
import psutil


class App:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Monitoring système")
        self.fenetre.resizable(False, False)

        # --- CPU ---
        self.frame_cpu = tk.LabelFrame(self.fenetre, text="CPU", padx=10, pady=10)
        self.frame_cpu.pack(fill=tk.X, padx=10, pady=5)
        self.label_cpu = tk.Label(self.frame_cpu, text="0%", font=("Arial", 24, "bold"))
        self.label_cpu.pack()
        self.canvas_cpu = tk.Canvas(self.frame_cpu, width=300, height=20, bg="white")
        self.canvas_cpu.pack()

        # --- RAM ---
        self.frame_ram = tk.LabelFrame(self.fenetre, text="RAM", padx=10, pady=10)
        self.frame_ram.pack(fill=tk.X, padx=10, pady=5)
        self.label_ram = tk.Label(self.frame_ram, text="0%", font=("Arial", 24, "bold"))
        self.label_ram.pack()
        self.canvas_ram = tk.Canvas(self.frame_ram, width=300, height=20, bg="white")
        self.canvas_ram.pack()

        # --- Disque ---
        self.frame_disque = tk.LabelFrame(self.fenetre, text="Disque", padx=10, pady=10)
        self.frame_disque.pack(fill=tk.X, padx=10, pady=5)
        self.label_disque = tk.Label(self.frame_disque, text="0%", font=("Arial", 24, "bold"))
        self.label_disque.pack()
        self.canvas_disque = tk.Canvas(self.frame_disque, width=300, height=20, bg="white")
        self.canvas_disque.pack()

        # --- Bouton Log ---
        self.log_active = True
        self.button_log= tk.Button(self.fenetre, text="Désactiver le log", command=self.toggle_log)
        self.button_log.pack(pady=10)

        self.rafraichir()
        self.fenetre.mainloop()

    def toggle_log(self):
        self.log_active = not self.log_active
        if self.log_active:
            self.button_log.config(text="Désactiver le log")
        else:
            self.button_log.config(text="Activer le log")

    def rafraichir(self):
        # Lire les métriques
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disque = psutil.disk_usage('/').percent

        # Mettre à jour CPU
        self.label_cpu.config(text=f"{cpu:.1f}%")
        self.canvas_cpu.delete("all")
        largeur_cpu = int(300 * cpu / 100)
        if cpu < 50:
            couleur_cpu = "green"
        elif cpu < 80:
            couleur_cpu = "orange"
        else:
            couleur_cpu = "red"
        self.canvas_cpu.create_rectangle(0, 0, largeur_cpu, 20, fill=couleur_cpu, outline="")

        # Mettre à jour RAM
        self.label_ram.config(text=f"{ram:.1f}%")
        self.canvas_ram.delete("all")
        largeur_ram = int(300 * ram / 100)
        if ram < 50:
            couleur_ram = "green"
        elif ram < 80:
            couleur_ram = "orange"
        else:
            couleur_ram = "red"
        self.canvas_ram.create_rectangle(0, 0, largeur_ram, 20, fill=couleur_ram, outline="")

        # Mettre à jour Disque
        self.label_disque.config(text=f"{disque:.1f}%")
        self.canvas_disque.delete("all")
        largeur_disque = int(300 * disque / 100)
        if disque < 50:
            couleur_disque = "green"
        elif disque < 80:
            couleur_disque = "orange"
        else:
            couleur_disque = "red"
        self.canvas_disque.create_rectangle(0, 0, largeur_disque, 20, fill=couleur_disque, outline="")

        # Écrire dans le fichier log
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ligne = (
            f"{horodatage} | "
            f"CPU: {cpu:.1f}% | "
            f"RAM: {ram:.1f}% | "
            f"Disque: {disque:.1f}%\n"
        )

        if self.log_active:
            with open("monitoring.log", 'a') as f:
                f.write(ligne)

        self.fenetre.after(2000, self.rafraichir)


if __name__ == "__main__":
    app = App()
