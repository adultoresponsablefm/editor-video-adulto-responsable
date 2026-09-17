"""Ensambla el programa limpio con animaciones y jingles exactos."""
import json, shutil, subprocess, tempfile
from pathlib import Path

ROOT=Path(r"C:\Users\noqui\Documents\Codex")
TRABAJO=ROOT/"trabajo_AR2"; ASSETS=ROOT/"assets"
SALIDA=TRABAJO/"programa_final_nivelado.mp4"
ANIM={"banner_inicio":ASSETS/"combinados"/"inicio_60fps.mp4","pausa_musical":ASSETS/"combinados"/"pausa_60fps.mp4","fin_transmision":ASSETS/"combinados"/"fin_60fps.mp4"}
JINGLE={"banner_inicio":ASSETS/"jingles_originales"/"Jingle Inicio XEHK Adulto Responsable.mp3","pausa_musical":ASSETS/"jingles_originales"/"jingle2  Pausas adulto responsable.mp3","fin_transmision":ASSETS/"jingles_originales"/"jingle Salida adulto responsable.mp3"}

def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)],text=True))
def run(args): subprocess.run(args,check=True)
def main():
    data=json.loads((TRABAJO/"cortes.json").read_text(encoding="utf-8")); source=Path(data["source"]); total=dur(source)
    cortes=sorted(data.get("cortes",[]),key=lambda x:x["start"])
    tmp=Path(tempfile.mkdtemp(prefix="ensamble_",dir=TRABAJO)); parts=[]
    try:
        cursor=0.0; n=0
        for c in cortes:
            a=max(cursor,float(c["start"])); b=min(total,float(c["end"])); razon=c["razon"]
            if a>cursor+0.05:
                out=tmp/f"parte_{n:03d}.mp4"; n+=1
                run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",f"{cursor:.3f}","-to",f"{a:.3f}","-i",str(source),"-map","0:v:0","-map","0:a:0?","-c:v","libx264","-preset","veryfast","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","aac","-ar","48000","-ac","2",str(out)]); parts.append(out)
            if razon in ANIM:
                video=ANIM[razon]; audio=JINGLE[razon]; length=dur(video); out=tmp/f"reemplazo_{n:03d}.mp4"; n+=1
                run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(video),"-i",str(audio),"-t",f"{length:.3f}","-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","veryfast","-r","60","-pix_fmt","yuv420p","-c:a","aac","-ar","48000","-ac","2","-shortest",str(out)]); parts.append(out)
            cursor=max(cursor,b)
        if cursor<total-0.05:
            out=tmp/f"parte_{n:03d}.mp4"; run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",f"{cursor:.3f}","-i",str(source),"-map","0:v:0","-map","0:a:0?","-c:v","libx264","-preset","veryfast","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","aac","-ar","48000","-ac","2",str(out)]); parts.append(out)
        lista=tmp/"concat.txt"; lista.write_text("\n".join("file '"+p.as_posix().replace("'","'\\''")+"'" for p in parts),encoding="utf-8")
        run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(lista),"-c","copy","-movflags","+faststart",str(SALIDA)])
        print(f"[OK] Resultado final: {SALIDA}")
    finally: shutil.rmtree(tmp,ignore_errors=True)
if __name__=="__main__": main()
