from flask import Flask, render_template
from flask_socketio import SocketIO
from web_app.blueprints.motor.motor_routes import motor_bp
import time
from threading import Thread

app = Flask(__name__)
app.register_blueprint(motor_bp)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('console_input')
def handle_input(message):
    # Here you can decide what to do with the received message
    print('Received command:', message)
    process_command(message)  # Custom function to process command


def process_command(command):
    # Dummy implementation to illustrate response
    if command == 'calibrate':
        calibrate()
        socketio.emit('console_output', 'Calibration started')


# Example function that might interact with your motor controller
def calibrate():
    # This should be replaced with the actual calibration function call
    socketio.emit('console_output', 'Calibration complete')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
