# Drone Autonomy Project

This project controls a drone using DroneKit and ArduPilot.  
The drone takes off, travels to a target GPS coordinate, slows down as it approaches, and hovers over the target.

This project was built as part of my Mechatronics final project.

## Features
- Autonomous takeoff to 10 meters altitude
- Cruise to target at 15 m/s
- Deceleration on approach
- GPS error tracking
- Manual takeover for landing
- Fully simulated flight support (SITL)

## Requirements
- Python 3.12+
- DroneKit
- pymavlink
- matplotlib

Install all dependencies with:
pip install -r requirements.txt


## How to Run
1. Activate your Python virtual environment:
    ```
    source ~/drone-env/bin/activate
    ```
2. Run the drone control script:
    ```
    python your_script_name.py
    ```

## Simulated Flight (SITL)
This project includes a dummy flight mode for testing without flying a real drone.

## License
MIT License - free for anyone to use or modify.

