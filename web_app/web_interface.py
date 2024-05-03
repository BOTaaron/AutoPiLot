from flask import Flask, request, render_template, jsonify
from web_app.blueprints.motor.motor_routes import motor_bp
import time
from threading import Thread

app = Flask(__name__)
app.register_blueprint(motor_bp)



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/enable-camera/<camera_type>')
def enable_camera(camera_type):
    return f"{camera_type} camera enabled", 200


@app.route('/disable-camera/<camera_type>')
def disable_camera(camera_type):
    return f"{camera_type} camera disabled", 200