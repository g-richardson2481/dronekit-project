import time
import math
import matplotlib.pyplot as plt

# ====== CONFIGURATION ======
TARGET_LAT = 37.123456
TARGET_LON = -122.123456
START_LAT = 37.122000
START_LON = -122.124000
ALTITUDE = 10  # Target altitude in meters
CLIMB_RATE = 2  # m/s

FAST_SPEED = 15  # m/s
SLOW_SPEED = 3   # m/s
DISTANCE_SLOWDOWN = 15  # meters
DISTANCE_HOVER = 3      # meters
LOG_INTERVAL = 0.5      # seconds
# ===========================

def get_distance_meters(lat1, lon1, lat2, lon2):
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return math.sqrt((dlat * 1.113195e5) ** 2 + (dlon * 1.113195e5) ** 2)

# Simulated drone state
current_lat = START_LAT
current_lon = START_LON
current_alt = 0  # start on ground

# Logs
distance_log = []
time_log = []
alt_log = []
lat_log = []
lon_log = []

start_time = time.time()
print("Simulated takeoff...")

# Simulate takeoff
while current_alt < ALTITUDE:
    current_alt += CLIMB_RATE * LOG_INTERVAL
    current_alt = min(current_alt, ALTITUDE)
    time_log.append(time.time() - start_time)
    distance_log.append(get_distance_meters(current_lat, current_lon, TARGET_LAT, TARGET_LON))
    alt_log.append(current_alt)
    lat_log.append(current_lat)
    lon_log.append(current_lon)
    time.sleep(LOG_INTERVAL)

print("Target altitude reached. Beginning horizontal travel...")

# Simulate horizontal flight
while True:
    distance = get_distance_meters(current_lat, current_lon, TARGET_LAT, TARGET_LON)
    distance_log.append(distance)
    alt_log.append(current_alt)
    time_log.append(time.time() - start_time)
    lat_log.append(current_lat)
    lon_log.append(current_lon)

    if distance <= DISTANCE_HOVER:
        print("Target reached (simulated).")
        break
    elif distance <= DISTANCE_SLOWDOWN:
        speed = SLOW_SPEED
    else:
        speed = FAST_SPEED

    # Direction vector
    delta_lat = TARGET_LAT - current_lat
    delta_lon = TARGET_LON - current_lon
    magnitude = math.sqrt(delta_lat**2 + delta_lon**2)
    step_lat = (speed * LOG_INTERVAL) * (delta_lat / magnitude) / 1.113195e5
    step_lon = (speed * LOG_INTERVAL) * (delta_lon / magnitude) / 1.113195e5

    current_lat += step_lat
    current_lon += step_lon
    time.sleep(LOG_INTERVAL)

# --- Plotting ---

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(time_log, distance_log)
plt.xlabel("Time (s)")
plt.ylabel("Distance to Target (m)")
plt.title("Distance Over Time")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(lon_log, lat_log, marker='o')
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Simulated Flight Path")
plt.grid()

plt.tight_layout()
plt.savefig("simulated_path_plot.png")
plt.show()
