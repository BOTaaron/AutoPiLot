import gpsd

import gpsd

class GPS:
    def __init__(self):
        gpsd.connect()

    def get_gps_data(self):
        try:
            packet = gpsd.get_current()
            if packet.mode >= 2:
                return {
                    "latitude": packet.lat,
                    "longitude": packet.lon,
                    "altitude": packet.alt if packet.mode >= 3 else None,
                    "speed": packet.hspeed,
                }
        except Exception as e:
            print(f"Error reading GPS data: {e}")
            return None

gps = GPS()

data = gps.get_gps_data()
print(data)
