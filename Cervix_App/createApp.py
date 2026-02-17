import os, textwrap

BASE = "cervix_flask_app"

FILES = {
    "app.py": r'''
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
''',

    "requirements.txt": "flask\nopencv-python\n",

    "README.md": "# Cervix Flask App\n\npython app.py\nhttp://localhost:5000\n",

    "templates/index.html": r'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Cervix App</title>
<link rel="stylesheet" href="/static/styles.css">
</head>
<body>
<div class="app">
  <div class="left">Panel de control</div>
  <div class="right">
    <img src="/video_feed">
    <canvas id="canvas"></canvas>
  </div>
</div>
<script src="/static/app.js"></script>
</body>
</html>
''',

    "static/styles.css": r'''
body { margin:0; background:#111; color:#eee; font-family:Arial; }
.app { display:flex; height:100vh; }
.left { width:350px; background:#222; padding:20px; }
.right { flex:1; position:relative; }
img, canvas { position:absolute; width:100%; height:100%; }
canvas { cursor:crosshair; }
''',

    "static/app.js": r'''
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

function resize(){
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
}
window.onresize = resize;
resize();

let draw=false, lx=0, ly=0;
canvas.onmousedown=e=>{draw=true;lx=e.offsetX;ly=e.offsetY;}
canvas.onmouseup=_=>draw=false;
canvas.onmousemove=e=>{
  if(!draw) return;
  ctx.strokeStyle="yellow";
  ctx.lineWidth=5;
  ctx.beginPath();
  ctx.moveTo(lx,ly);
  ctx.lineTo(e.offsetX,e.offsetY);
  ctx.stroke();
  lx=e.offsetX; ly=e.offsetY;
}
'''
}

for path, content in FILES.items():
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))

print("✅ Proyecto cervix_flask_app creado correctamente")
