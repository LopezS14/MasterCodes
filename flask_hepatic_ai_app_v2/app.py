from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
import os

# importar funciones del módulo de clasificación
from classifier_module import (
    UPLOAD_FOLDER,
    allowed_file,
    procesar_y_predecir,
    CLASES,
)

app = Flask(__name__)
app.secret_key = "cambia-esta-clave"
app.permanent_session_lifetime = timedelta(hours=8)

USERS = {
    "user": generate_password_hash("123456"),
    "admin": generate_password_hash("admin123"),
}


def login_required(f):
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("menu") if session.get("user") else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pwd = request.form.get("password", "")
        if user in USERS and check_password_hash(USERS[user], pwd):
            session.permanent = True
            session["user"] = user
            flash("Access granted", "success")
            return redirect(url_for("menu"))
        flash("Usuario o contraseña inválidos", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html", user=session["user"])


# ===== CLASIFICADOR: opción Start Pre-diagnosis =====
@app.route("/prediagnostico", methods=["GET", "POST"])
@login_required
def evaluar():
    from classifier_module import (
        UPLOAD_FOLDER,
        allowed_file,
        procesar_y_predecir,
    )

    pred_clase = None
    resultado = None
    image_url = None
    diagnostico = None  # <- texto lado derecho

    if request.method == "POST":
        if "file" not in request.files:
            flash("No se recibió archivo.", "danger")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("Debes seleccionar una imagen.", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                # procesar imagen y obtener clase + texto resumen
                pred_clase, resultado = procesar_y_predecir(filepath)
                image_url = url_for("static", filename=f"uploads/{filename}")

                # ===== diagnóstico en texto =====
                if pred_clase in ["2w", "8w", "12w"]:
                    diagnostico = (
                        f"Prediagnosis: Fatty Liver.\n\n"
                        f"The sample was classified as week {pred_clase}, "
                        "which corresponds to tissue with the presence of fatty liver."
                    )
                elif pred_clase == "Control":
                    diagnostico = (
                        "Prediagnosis: Healthy Liver.\n\n"
                        "The sample was classified as week Control, "
                        "which corresponds to tissue with no evidence of fatty liver."
                    )
                else:
                    diagnostico = (
                        "It was not possible to determine the prediagnosis based on the predicted class."
                    )
                # ================================
            except Exception as e:
                flash(f"Error procesando la imagen: {e}", "danger")
        else:
            flash("Tipo de archivo no permitido. Usa PNG, JPG o JPEG.", "danger")

    return render_template(
        "classifier.html",
        titulo="Starting model classification",
        pred_clase=pred_clase,
        resultado=resultado,
        image_url=image_url,
        diagnostico=diagnostico,  # <- se envía al template
    )


# ====================================================
@app.route("/calculator")
@login_required
def calculator():
    return render_template("calculator.html")


@app.route("/resultados")
@login_required
def resultados():
    return render_template(
        "stub.html",
        titulo="Resultados",
        texto="Aquí van tus resultados y descargas.",
    )


if __name__ == "__main__":
    app.run(debug=True)
