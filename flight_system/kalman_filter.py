import numpy as np

class KalmanFilterOrientation:
    """
    a Kalman filter for estimating the orientation of the plane using data from the
    accelerometer, gyroscope, and magnetometer
    """
    def __init__(self, dt):
        """
        Initialise the kalman filter

        Parameters:
            dt (float): Time between filter updates
        """
        self.dt = dt
        self.A = np.eye(6)
        self.B = np.zeros((6, 3))
        self.H = np.zeros((3, 6))
        self.H[:3, :3] = np.eye(3)
        self.Q = np.eye(6) * 0.1
        self.R = np.eye(3) * 0.1
        self.P = np.eye(6)
        self.x = np.zeros((6, 1))
        self.u = np.zeros((3, 1))

    def predict(self):
        """
        Predict the next state and update the estimate error covariance matrix
        """
        self.x = self.A @ self.x + self.B @ self.u
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, z):
        """
        Update the state estimate using the measurement z

        Parameters:
            z (numpy.ndarray): Measurement vector
        """
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(6) - K @ self.H) @ self.P

    def update_orientation(self, acc, gyr, mag):
        """
        Update the orientation estimate using the accelerometer, gyroscope, and magnetometer 

        Parameters:
        acc (numpy.ndarray): Accelerometer data (3 elements: x, y, z).
        gyr (numpy.ndarray): Gyroscope data (3 elements: x, y, z).
        mag (numpy.ndarray): Magnetometer data (3 elements: x, y, z).

        Returns:
        tuple: The estimated roll, pitch, and yaw angles in degrees.
        """
        self.u = gyr.reshape((3, 1))
        self.predict()

        z = acc.reshape((3, 1))
        self.update(z)

        roll = np.arctan2(self.x[1], self.x[2])
        pitch = np.arctan2(-self.x[0], np.sqrt(self.x[1]**2 + self.x[2]**2))
        yaw = np.arctan2(mag[1], mag[0])  # Simplified yaw calculation

        roll_deg = np.degrees(roll).item()
        pitch_deg = np.degrees(pitch).item()
        yaw_deg = np.degrees(yaw).item()

        return roll_deg, pitch_deg, yaw_deg
