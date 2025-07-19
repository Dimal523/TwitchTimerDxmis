from flask import Flask, jsonify, render_template_string
from datetime import datetime, timedelta
import os

app = Flask(__name__)

TIMER_FILE = "timer.txt"
TIME_INCREMENT = timedelta(minutes=30)

def get_current_time():
    if os.path.exists(TIMER_FILE):
        with open(TIMER_FILE, "r") as f:
            time_str = f.read().strip()
            try:
                return datetime.fromisoformat(time_str)
            except Exception:
                pass
    return datetime.now()

def save_time(new_time):
    with open(TIMER_FILE, "w") as f:
        f.write(new_time.isoformat())

@app.route("/")
def home():
    return "Timer Service Running"

@app.route("/addtime")
def add_time():
    current_time = get_current_time()
    now = datetime.now()

    if current_time < now:
        current_time = now

    new_time = current_time + TIME_INCREMENT
    save_time(new_time)

    return jsonify({
        "message": f"⏱️ Timer extended! New end time: {new_time.strftime('%H:%M:%S')}."
    })

TIMER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Timer</title>
    <style>
        body {
            background-color: rgba(0,0,0,0);
            color: white;
            font-size: 48px;
            font-family: 'Courier New', monospace;
            text-align: center;
            margin-top: 20%;
        }
    </style>
</head>
<body>
    <div id="timer">Loading...</div>
    <script>
        async function getTime() {
            const res = await fetch('/gettime');
            const data = await res.json();
            return new Date(data.end_time);
        }

        function updateCountdown(targetTime) {
            const now = new Date();
            let diff = (targetTime - now) / 1000;
            if (diff < 0) diff = 0;

            const hours = Math.floor(diff / 3600);
            const minutes = Math.floor((diff % 3600) / 60);
            const seconds = Math.floor(diff % 60);

            document.getElementById('timer').textContent =
                `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        }

        let targetTime;
        getTime().then(time => {
            targetTime = time;
            updateCountdown(targetTime);
            setInterval(() => updateCountdown(targetTime), 1000);
        });
    </script>
</body>
</html>
"""

@app.route("/timer")
def show_timer():
    return render_template_string(TIMER_TEMPLATE)
    return jsonify({
    "message": f"⏱️ Timer extended! New end time: {new_time.isoformat()}."
})


@app.route("/gettime")
def get_time():
    target = get_current_time()
    return jsonify({"end_time": target.isoformat()})

@app.route("/reset")
def reset_timer():
    new_time = datetime.now() + timedelta(hours=3)
    print(f"[DEBUG] Resetting timer to: {new_time.isoformat()}")
    save_time(new_time)
    return jsonify({
        "message": f"⏱️ Timer reset to 3 hours from now: {new_time.strftime('%H:%M:%S')}."
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
