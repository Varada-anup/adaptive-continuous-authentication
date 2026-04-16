from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from decision_engine import DecisionEngine
import numpy as np

app = Flask(__name__)
app.secret_key = "secret_key"

engine = DecisionEngine()

CALIBRATION_SAMPLES_REQUIRED = 20

calibration_counts = {}
is_calibrating = {}

# ---------------- FEATURE EXTRACTION ----------------

def extract_features(keys, mouse):
    typing_speeds = []
    hold_times = []

    for k in keys:
        hold = (k["up"] - k["down"]) / 1000
        hold_times.append(hold)

    for i in range(1, len(keys)):
        interval = (keys[i]["down"] - keys[i-1]["up"]) / 1000
        typing_speeds.append(interval)

    mouse_speeds = []

    for i in range(1, len(mouse)):
        dx = mouse[i]["x"] - mouse[i-1]["x"]
        dy = mouse[i]["y"] - mouse[i-1]["y"]
        dt = (mouse[i]["time"] - mouse[i-1]["time"]) / 1000

        if dt > 0:
            speed = ((dx**2 + dy**2)**0.5) / dt
            mouse_speeds.append(speed)

    avg_hold = np.mean(hold_times) if hold_times else 0
    avg_type = np.mean(typing_speeds) if typing_speeds else 0
    avg_mouse = np.mean(mouse_speeds) if mouse_speeds else 0

    avg_mouse = avg_mouse / 1000
    avg_type = avg_type * 2

    return [avg_hold, avg_type, avg_mouse]

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username

        engine.reset_user(username)

        if username not in engine.user_profiles:
            engine.start_calibration(username)
            calibration_counts[username] = 0
            is_calibrating[username] = True
        else:
            is_calibrating[username] = False

        return redirect(url_for("interaction"))

    return render_template("login.html")

@app.route("/interaction")
def interaction():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("interaction.html")

# ---------------- CAPTURE ----------------

@app.route("/capture", methods=["POST"])
def capture():
    if "username" not in session:
        return jsonify({"status": "error"})

    username = session["username"]
    data = request.json

    keys = data.get("keys", [])
    mouse = data.get("mouse", [])

    if len(keys) < 5:
        return jsonify({"status": "learning", "decision": "learning"})

    features = extract_features(keys, mouse)

    decision, score = engine.authenticate(username, features)

    if decision == "intruder":
        session.clear()
        return jsonify({
            "status": "intruder",
            "decision": "intruder",
            "score": score,
            "redirect": "/login"
        })

    return jsonify({
        "status": decision,
        "decision": decision,
        "score": score
    })

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)