import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, Response, request, jsonify
import cv2, threading

app = Flask(__name__)

cap = None
lock = threading.Lock()

def get_camera(index=0):
    global cap
    with lock:
        if cap is None:
            cap = cv2.VideoCapture(index)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cap

def gen_frames():
    cam = get_camera(0)
    while True:
        ok, frame = cam.read()
        if not ok:
            continue
        ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not ok:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame")

STATE = {"connected": False, "intensity": 0, "light": "Blanco"}
CAPTURES_ROOT = Path("captures")  # carpeta base donde se guardará todo
CAPTURES_ROOT.mkdir(exist_ok=True)

def safe_folder(name: str) -> str:
    # solo letras, numeros, guion, guion_bajo
    name = (name or "").strip()
    name = "".join(ch for ch in name if ch.isalnum() or ch in ("-", "_"))
    return name or "default"

@app.post("/api/capture")
def api_capture():
    data = request.get_json(force=True) or {}
    folder = safe_folder(data.get("folder", "default"))

    cam = get_camera(0)
    ok, frame = cam.read()
    if not ok:
        return jsonify({"ok": False, "error": "No se pudo leer de la cámara"}), 500

    out_dir = CAPTURES_ROOT / folder
    out_dir.mkdir(parents=True, exist_ok=True)

    # nombre: IMG_YYYYmmdd_HHMMSS_mmm.jpg
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"IMG_{ts}.jpg"
    out_path = out_dir / filename

    ok = cv2.imwrite(str(out_path), frame)
    if not ok:
        return jsonify({"ok": False, "error": "No se pudo guardar la imagen"}), 500

    return jsonify({
        "ok": True,
        "folder": folder,
        "filename": filename,
        "path": str(out_path)
    })


@app.post("/api/connect")
def connect():
    STATE["connected"] = True
    return jsonify(STATE)

@app.post("/api/disconnect")
def disconnect():
    STATE["connected"] = False
    return jsonify(STATE)

@app.post("/api/light")
def light():
    STATE["light"] = request.json.get("light", "Blanco")
    return jsonify(STATE)

@app.post("/api/intensity")
def intensity():
    STATE["intensity"] = int(request.json.get("intensity", 0))
    return jsonify(STATE)

if __name__ == "__main__":
    app.run(debug=True)
