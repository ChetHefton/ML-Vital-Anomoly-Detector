from flask import Flask, jsonify, render_template
import threading
import time
import random

import hr
import ox
import respRate
import temp

app = Flask(__name__)

#shared vitals state (simple + effective for one-process dev server)
vitals = {
    "hr": random.randint(60, 100),
    "spo2": round(random.uniform(95.0, 100.0), 1),
    "rr": random.randint(12, 20),
    "temp_f": round(random.uniform(97.0, 99.0), 1),
    "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
}

lock = threading.Lock()

def updater_loop():
    """Continuously update vitals once per second."""
    while True:
        with lock:
            vitals["hr"] = hr.updateHR(vitals["hr"])
            vitals["spo2"] = ox.updateOx(vitals["spo2"])
            vitals["rr"] = respRate.updateRespRate(vitals["rr"])
            vitals["temp_f"] = temp.updateTemp(vitals["temp_f"])
            vitals["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")

        time.sleep(1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/vitals")
def api_vitals():
    with lock:
        return jsonify(vitals)

if __name__ == "__main__":
    t = threading.Thread(target=updater_loop, daemon=True)
    t.start()

    #Run Flask
    app.run(host="127.0.0.1", port=5000, debug=True)