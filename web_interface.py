from flask import Flask, render_template, jsonify
import time
from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# Dummy data - replace with real data retrieval logic
motor_output_data = {
    'motor_output': 1200  # Replace with real motor output retrieval logic
}

@app.route('/data/motor-output')
def motor_output():
    return jsonify(motor_output_data)


@app.route('/enable-camera/<camera_type>')
def enable_camera(camera_type):
    return f"{camera_type} camera enabled", 200


@app.route('/disable-camera/<camera_type>')
def disable_camera(camera_type):
    return f"{camera_type} camera disabled", 200