import time
import math
import matplotlib.pyplot as plt

# ====== CONFIGURATION ======
TARGET_LAT = 37.123456
TARGET_LON = -122.123456
START_LAT = 37.122000
START_LON = -122.124000
FAST_SPEED = 15  # m/s
SLOW_SPEED = 3   # m/s
DISTANCE_SLOWDOWN = 15  # meters
DISTANCE_HOVER = 3      # meters
LOG_INTERVAL = 0.5      # seconds
SIM_STEP = LOG_INTERVAL  # seconds per simulation update
# ===========================

def get_distance_meters(lat1, lon1, lat2, lon2):
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return math.sqrt((dlat * 1.113195e5) ** 2 + (dlon * 1.113195e5) ** 2)

# Simulate location
current_lat = START_LAT
current_lon = START_LON

distance_log = []
time_log = []
start_time = time.time()

print("Starting dummy flight simulation...")

while True:
    distance = get_distance_meters(current_lat, current_lon, TARGET_LAT, TARGET_LON)
    distance_log.append(distance)
    time_log.append(time.time() - start_time)

    if distance <= DISTANCE_HOVER:
        print("Target reached (simulated).")
        break
    elif distance <= DISTANCE_SLOWDOWN:
        speed = SLOW_SPEED
    else:
        speed = FAST_SPEED

    # Calculate direction vector
    delta_lat = TARGET_LAT - current_lat
    delta_lon = TARGET_LON - current_lon
    magnitude = math.sqrt(delta_lat**2 + delta_lon**2)
    step_lat = (speed * SIM_STEP) * (delta_lat / magnitude) / 1.113195e5
    step_lon = (speed * SIM_STEP) * (delta_lon / magnitude) / 1.113195e5

    current_lat += step_lat
    current_lon += step_lon

    time.sleep(LOG_INTERVAL)

# Plot the results
plt.plot(time_log, distance_log)
plt.xlabel("Time (s)")
plt.ylabel("Distance to Target (m)")
plt.title("Simulated GPS Distance Over Time")
plt.grid()
plt.savefig("simulated_distance_plot.png")
plt.show()
