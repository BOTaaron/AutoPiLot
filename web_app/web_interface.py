import os
from flask import Flask, render_template
from extensions import socketio
from web_app.routes.motor_routes import create_motor_routes
from web_app.routes.camera_routes import camera_bp
from web_app.routes.data_routes import create_data_routes
from web_app.routes.map_routes import maps_bp
from web_app.blueprints.motor.motor_manager import get_motor_controller
from dash_app import app as dash_app

app = Flask(__name__)

app.register_blueprint(camera_bp)
app.register_blueprint(maps_bp)
socketio.init_app(app, async_mode='threading')
motor = get_motor_controller(socketio)

motor_bp = create_motor_routes(socketio)
app.register_blueprint(motor_bp)

data_bp = create_data_routes(socketio)
app.register_blueprint(data_bp)

dash_app.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('console_input')
def handle_input(message):
    print('Received command:', message)
    process_command(message)


def process_command(command):

    if motor.calibration_active and command.strip() == '':
        motor.handle_empty_command()
        return
    # Calibrates the motor
    if command == 'calibrate':
        motor.calibrate()
        socketio.emit('console_output', 'Calibration started')
    elif command == 'arm':
        motor.arm()
        socketio.emit('console_output', 'Arming motor...')
    elif command.startswith('power '):
        try:
            power_percentage = int(command.split()[1])
            motor.go(power_percentage)
            socketio.emit('console_output', f'Setting motor power to {power_percentage}%')
        except (IndexError, ValueError):
            socketio.emit('console_output', 'Invalid power command. Use "power <percentage>".')
    elif command == 'stop':
        motor.stop()
        socketio.emit('console_output', 'Stopping motor...')
    else:
        socketio.emit('console_output', 'Unknown command')


"""
To run the app, first launch the map server: mbtileserver --dir ~/repositories/AutoPiLot/web_app/map_tiles --port 8000
http://aaron.local:5000/ to view page
"""
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
