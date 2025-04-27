from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import math
import matplotlib.pyplot as plt

# ====== CONFIGURATION ======
TARGET_LAT = 37.123456  # Replace with actual lat
TARGET_LON = -122.123456  # Replace with actual lon
ALTITUDE = 10  # meters
FAST_SPEED = 15  # m/s
SLOW_SPEED = 3   # m/s
DISTANCE_SLOWDOWN = 15  # meters
DISTANCE_HOVER = 3      # meters
LOG_INTERVAL = 0.5      # seconds
# ===========================

# Connect to vehicle
print("Connecting...")
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=57600)

def get_distance_meters(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*1.113195e5)**2 + (dlong*1.113195e5)**2)

def arm_and_takeoff(target_alt):
    print("Arming motors...")
    while not vehicle.is_armable:
        time.sleep(1)
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        time.sleep(1)
    print(f"Taking off to {target_alt} meters...")
    vehicle.simple_takeoff(target_alt)
    while True:
        if vehicle.location.global_relative_frame.alt >= target_alt * 0.95:
            break
        time.sleep(1)
    print("Reached target altitude.")

def send_velocity(velocity_x, velocity_y, velocity_z):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,  # time_boot_ms, target IDs
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # Relative to vehicle's body frame
        0b0000111111000111,  # Only velocity enabled
        0, 0, 0,  # x, y, z positions
        velocity_x, velocity_y, velocity_z,
        0, 0, 0,  # acceleration
        0, 0)  # yaw, yaw_rate
    vehicle.send_mavlink(msg)
    vehicle.flush()

# --- Start Flight Sequence ---
arm_and_takeoff(ALTITUDE)

target_location = LocationGlobalRelative(TARGET_LAT, TARGET_LON, ALTITUDE)
distance_log = []
time_log = []

start_time = time.time()
print("Beginning flight toward target...")

while True:
    current_location = vehicle.location.global_relative_frame
    distance = get_distance_meters(current_location, target_location)
    distance_log.append(distance)
    time_log.append(time.time() - start_time)

    if distance <= DISTANCE_HOVER:
        print("Target reached. Switching to LOITER.")
        vehicle.mode = VehicleMode("LOITER")
        break
    elif distance <= DISTANCE_SLOWDOWN:
        speed = SLOW_SPEED
    else:
        speed = FAST_SPEED

    # Calculate direction vector
    delta_lat = TARGET_LAT - current_location.lat
    delta_lon = TARGET_LON - current_location.lon
    magnitude = math.sqrt(delta_lat**2 + delta_lon**2)
    vx = speed * (delta_lat / magnitude)
    vy = speed * (delta_lon / magnitude)
    send_velocity(vx, vy, 0)

    time.sleep(LOG_INTERVAL)

# Save and plot distance over time
plt.plot(time_log, distance_log)
plt.xlabel("Time (s)")
plt.ylabel("Distance to Target (m)")
plt.title("GPS Distance to Target Over Time")
plt.grid()
plt.savefig("distance_plot.png")
plt.show()

# Done!
print("Mission complete. Waiting for manual takeover...")
