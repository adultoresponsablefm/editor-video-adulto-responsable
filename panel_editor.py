import os
import queue
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parent
PS1 = ROOT / "iniciar_editor.ps1"
OUTPUT = ROOT / "trabajo_AR2" / "programa_final_nivelado.mp4"


class EditorPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor local · Adulto Responsable")
        self.root.geometry("620x260")
        self.video = tk.StringVar()
        self.status = tk.StringVar(value="Selecciona un video para comenzar.")
        self.events = queue.Queue()

        frame = ttk.Frame(root, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Video de entrada").pack(anchor="w")
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(5, 14))
        ttk.Entry(row, textvariable=self.video).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Cargar video…", command=self.choose).pack(side="left", padx=(8, 0))
        self.start_button = ttk.Button(frame, text="Iniciar edición", command=self.start)
        self.start_button.pack(fill="x", ipady=6)
        ttk.Button(frame, text="Abrir DaVinci Resolve", command=self.open_resolve).pack(fill="x", pady=(8, 0))
        ttk.Label(frame, textvariable=self.status, wraplength=580).pack(anchor="w", pady=(16, 0))
        self.root.after(250, self.poll)

    def choose(self):
        path = filedialog.askopenfilename(title="Seleccionar video", filetypes=[("Videos", "*.mp4 *.mov *.mkv *.avi"), ("Todos", "*.*")])
        if path:
            self.video.set(path)
            self.status.set("Video cargado. Pulsa Iniciar edición.")

    def open_resolve(self):
        candidates = [
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Blackmagic Design/DaVinci Resolve/Resolve.exe",
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Blackmagic Design/DaVinci Resolve/fusion/Resolve.exe",
        ]
        exe = next((p for p in candidates if p.exists()), None)
        if not exe:
            messagebox.showerror("DaVinci Resolve", "No encontré Resolve.exe. Ábrelo manualmente o configura la ruta.")
            return
        subprocess.Popen([str(exe)])
        self.status.set("DaVinci está iniciando. En Resolve activa Workspace > Scripts > resolve_bridge una vez.")

    def start(self):
        video = self.video.get().strip()
        if not video or not Path(video).exists():
            messagebox.showwarning("Falta el video", "Carga primero un archivo de video válido.")
            return
        self.start_button.configure(state="disabled")
        self.status.set("Iniciando DaVinci y preparando el procesamiento…")
        self.open_resolve()
        threading.Thread(target=self.run_pipeline, args=(video,), daemon=True).start()

    def run_pipeline(self, video):
        try:
            result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(PS1), "-Video", video], cwd=ROOT, text=True, capture_output=True)
            if result.returncode:
                raise RuntimeError(result.stderr.strip() or result.stdout.strip())
            if not OUTPUT.exists():
                raise RuntimeError("El procesamiento terminó sin generar el archivo final.")
            self.events.put(("ok", "Procesamiento terminado. Audio y video fueron exportados. Activa el puente si Resolve lo solicita y ejecuta la importación."))
        except Exception as exc:
            self.events.put(("error", f"No se pudo completar: {exc}"))

    def poll(self):
        try:
            kind, text = self.events.get_nowait()
            self.status.set(text)
            self.start_button.configure(state="normal")
            if kind == "error":
                messagebox.showerror("Editor local", text)
        except queue.Empty:
            pass
        self.root.after(250, self.poll)


if __name__ == "__main__":
    app = tk.Tk()
    EditorPanel(app)
    app.mainloop()
