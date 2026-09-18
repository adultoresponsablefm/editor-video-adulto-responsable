"""Detector visual de plecas, con muestreo fino para límites precisos."""
import json, os, shutil, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(r"C:\Users\noqui\Documents\Codex"); TRABAJO=ROOT/"trabajo_AR2"; SALIDA=TRABAJO/"cortes.json"; REF=ROOT/"assets"/"referencias"; UMBRAL=.16; MUESTREO=10
REFS={
    "banner_inicio.png":"banner_inicio", "banner_inicio_v2.png":"banner_inicio", "banner_inicio_original.png":"banner_inicio",
    "banner_pausa_musical.png":"pausa_musical", "banner_pausa_musical_original.png":"pausa_musical",
    "banner_fin_transmision.png":"fin_transmision", "banner_fin_transmision_original.png":"fin_transmision",
    "chilaquil/inicio.png":"banner_inicio", "chilaquil/inicio_overlay.png":"banner_inicio",
    "chilaquil/fin_overlay.png":"fin_transmision", "chilaquil/fin_transmision.png":"fin_transmision"
}
def limpiar_versiones_anteriores():
    for p in list(TRABAJO.glob("frames_detector_*"))+list(TRABAJO.glob("deteccion_*")):
        if p.is_dir(): shutil.rmtree(p,ignore_errors=True)
def cargar_referencias():
    out={}
    for n,r in REFS.items():
        p=REF/n
        if p.exists(): out[r]=np.asarray(Image.open(p).convert("RGB").resize((160,90)),dtype=np.float32)/255
        else: print(f"[!] Falta referencia: {p}")
    return out
def detectar(video,refs):
    tmp=Path(tempfile.mkdtemp(prefix="frames_detector_",dir=TRABAJO))
    try:
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-i",str(video),"-vf",f"fps={MUESTREO},scale=160:90:force_original_aspect_ratio=decrease,pad=160:90:(ow-iw)/2:(oh-ih)/2","-q:v","4",str(tmp/"%07d.jpg")],check=True)
        hits=[]
        for f in sorted(tmp.glob("*.jpg")):
            t=(int(f.stem)-1)/MUESTREO; frame=np.asarray(Image.open(f).convert("RGB"),dtype=np.float32)/255
            razon,error=min(((r,float(np.mean(np.abs(frame-v)))) for r,v in refs.items()),key=lambda x:x[1])
            if error<=UMBRAL: hits.append((t,razon,error))
        bloques=[]
        for t,razon,error in hits:
            if bloques and razon==bloques[-1]["razon"] and t<=bloques[-1]["end"]+.25:
                bloques[-1]["end"]=t+1/MUESTREO; bloques[-1]["error"]=min(bloques[-1]["error"],error)
            else: bloques.append({"start":max(0,t-1/MUESTREO),"end":t+1/MUESTREO,"razon":razon,"error":error})
        return [{"start":round(b["start"],2),"end":round(b["end"],2),"duracion":round(b["end"]-b["start"],2),"razon":b["razon"],"fuente":"comparacion_visual","similitud":round(1-b["error"],4)} for b in bloques if b["end"]-b["start"]>=2]
    finally: shutil.rmtree(tmp,ignore_errors=True)
def main():
    candidatos=[]
    if os.environ.get("EDITOR_VIDEO"): candidatos.append(Path(os.environ["EDITOR_VIDEO"]))
    candidatos += [Path(r"C:\Users\noqui\OneDrive\Desktop\Adulto Responsable\Backup Programas\Adulto Responsable 13062026.mp4"),Path(r"C:\Users\noqui\Videos\Porgramas grabados Radio Chilaquil\Adulto Responsable 13062026.mp4")]; video=next((p for p in candidatos if p.exists()),None)
    if not video: raise FileNotFoundError("No se encontró el video fuente")
    TRABAJO.mkdir(parents=True,exist_ok=True); limpiar_versiones_anteriores(); total=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(video)],text=True)); cortes=detectar(video,cargar_referencias())
    for c in cortes: print(f"[!] {c['razon']}: {c['start']:.1f}s -> {c['end']:.1f}s")
    SALIDA.write_text(json.dumps({"source":str(video),"fps":60.0,"duration":total,"total_cortes":len(cortes),"cortes":cortes},ensure_ascii=False,indent=2),encoding="utf-8"); print(f"[OK] Guardado {SALIDA}: {len(cortes)} bloques")
if __name__=="__main__": main()
