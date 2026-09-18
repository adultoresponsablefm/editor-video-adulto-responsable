"""Detecta bloques sin locutor para el perfil Radio Chilaquil."""
import json, os, subprocess
from pathlib import Path
import cv2

ROOT=Path(r"C:\Users\noqui\Documents\Codex"); TRABAJO=ROOT/"trabajo_AR2"; SALIDA=TRABAJO/"cortes.json"
MODELO=ROOT/"2026-09-14"/"realtime-voice-chat"/"trabajo_2026-09-15_v2"/"face_detection_yunet_2023mar.onnx"
REFERENCIA=ROOT/"assets"/"referencias"/"locutor_chilaquil.jpg"

def main():
    src=os.environ.get("EDITOR_VIDEO")
    if not src or not Path(src).exists(): raise FileNotFoundError("Define EDITOR_VIDEO con el MP4 de Chilaquil")
    cap=cv2.VideoCapture(src); fps=cap.get(cv2.CAP_PROP_FPS) or 60; total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); duration=total/fps; step=max(1,int(fps*2))
    if not MODELO.exists(): raise FileNotFoundError(f"Falta modelo facial: {MODELO}")
    detector=cv2.FaceDetectorYN.create(str(MODELO),"",(320,180),0.7,0.3,500); rows=[]
    ref=cv2.imread(str(REFERENCIA)); ref=cv2.resize(ref,(320,180)); detector.setInputSize((320,180)); _,rf=detector.detect(ref)
    if rf is None or len(rf)==0: raise RuntimeError("No se detectó el rostro en locutor_chilaquil.jpg")
    x,y,w,h=[int(v) for v in rf[0][:4]]; ref_face=cv2.resize(ref[max(0,y):y+h,max(0,x):x+w],(100,100)); orb=cv2.ORB_create(nfeatures=500); kp_ref,des_ref=orb.detectAndCompute(cv2.cvtColor(ref_face,cv2.COLOR_BGR2GRAY),None)
    # Calibración con el primer rostro del propio video: compensa cambios de cámara.
    cap.set(cv2.CAP_PROP_POS_FRAMES,0); ok,first=cap.read()
    overlay_ref=None
    if ok:
        first=cv2.resize(first,(320,180)); overlay_ref=first[145:180].copy(); detector.setInputSize((320,180)); _,ff=detector.detect(first)
        if ff is not None and len(ff):
            x,y,w,h=[int(v) for v in ff[0][:4]]; crop=first[max(0,y):y+h,max(0,x):x+w]
            if crop.size: kp_ref,des_ref=orb.detectAndCompute(cv2.cvtColor(cv2.resize(crop,(100,100)),cv2.COLOR_BGR2GRAY),None)
    for n in range(0,total,step):
        cap.set(cv2.CAP_PROP_POS_FRAMES,n); ok,frame=cap.read()
        if not ok: continue
        small=cv2.resize(frame,(320,180)); detector.setInputSize((320,180)); _,faces=detector.detect(small); faces=[] if faces is None else faces
        same=False
        # La pleca inferior Chilaquil es persistente cuando está el locutor.
        # Se usa como señal primaria y evita confundir rostros de videoclips.
        if overlay_ref is not None and float(cv2.absdiff(small[145:180],overlay_ref).mean())/255.0 < 0.05: same=True
        for face in faces:
            x,y,w,h=[int(v) for v in face[:4]]; crop=small[max(0,y):y+h,max(0,x):x+w]
            if crop.size==0 or des_ref is None: continue
            kp,des=orb.detectAndCompute(cv2.cvtColor(cv2.resize(crop,(100,100)),cv2.COLOR_BGR2GRAY),None)
            if des is None: continue
            matches=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(des_ref,des,k=2); good=[m for m,n2 in matches if m.distance<.75*n2.distance]
            if len(good)>=8: same=True; break
        rows.append((n/fps,1 if same else 0))
    cap.release()
    cortes=[]; start=None
    for t,count in rows:
        if count==0 and start is None: start=t
        if count>0 and start is not None:
            if t-start>=4: cortes.append({"start":round(start,2),"end":round(t,2),"duracion":round(t-start,2),"razon":"sin_locutor","fuente":"deteccion_facial"})
            start=None
    if start is not None and duration-start>=4: cortes.append({"start":round(start,2),"end":round(duration,2),"duracion":round(duration-start,2),"razon":"sin_locutor","fuente":"deteccion_facial"})
    if len(cortes)==1 and cortes[0]["start"]==0 and cortes[0]["end"]>=duration-1: raise RuntimeError("El detector no reconoció al locutor; no se generará un corte total")
    TRABAJO.mkdir(parents=True,exist_ok=True); SALIDA.write_text(json.dumps({"source":src,"fps":fps,"duration":duration,"total_cortes":len(cortes),"perfil":"Radio Chilaquil","cortes":cortes},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"[OK] {len(cortes)} bloques sin locutor guardados en {SALIDA}")
if __name__=="__main__": main()
