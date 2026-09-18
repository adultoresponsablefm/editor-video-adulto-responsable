"""Importa el resultado final a DaVinci Resolve y activa su timeline."""
import csv, json, subprocess
from pathlib import Path
from resolve_client import BridgeClient

ROOT = Path(r"C:\Users\noqui\Documents\Codex")
VIDEO = ROOT / "trabajo_AR2" / "programa_final_nivelado.mp4"
NOMBRE = "Programa Final - REVISION FINAL"

def handle(value):
    return value.get("__handle__") if isinstance(value, dict) else value

def main():
    if not VIDEO.exists():
        raise FileNotFoundError(f"No existe el archivo final: {VIDEO}")
    probe = subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type","-of","csv=p=0",str(VIDEO)], capture_output=True, text=True, check=True)
    tracks = {x.strip() for x in probe.stdout.splitlines()}
    if not {"video", "audio"}.issubset(tracks):
        raise RuntimeError(f"No se importó: el archivo debe tener video y audio. Pistas encontradas: {sorted(tracks)}")
    print("[OK] Archivo validado: contiene video y audio")
    c = BridgeClient.from_config()
    pm = handle(c.call("GetProjectManager", target="resolve"))
    project = handle(c.call("GetCurrentProject", target=pm))
    pool = handle(c.call("GetMediaPool", target=project))

    # Solo elimina revisiones creadas por este flujo; no toca otras timelines.
    old = []
    count = int(c.call("GetTimelineCount", target=project))
    for index in range(1, count + 1):
        timeline = c.call("GetTimelineByIndex", index, target=project)
        if str(c.call("GetName", target=handle(timeline))).startswith("Programa Final - REVISION"):
            old.append(timeline)
    if old:
        c.call("DeleteTimelines", old, target=pool)

    item = c.call("ImportMedia", [str(VIDEO)], target=pool)[0]
    c.call("CreateTimelineFromClips", NOMBRE, [item], target=pool)
    result = c.dispatch("set_current_timeline", {"timeline_name": NOMBRE})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[OK] Timeline activa: {NOMBRE}")

if __name__ == "__main__":
    main()
