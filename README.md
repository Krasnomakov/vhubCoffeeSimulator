## Overview
This repository contains files representing iterations in the simulation development process. The final result is located in the "simulation2" folder, with the main file being "v4_simulationWithCases.py". Sample event logs are stored inside folders.

**Demo:** https://vimeo.com/883906069/c506d45580

## Simulation Overview
The code simulates the daily activities of users within a facility. Users move between different rooms, consume coffee, and respond to messages from an autonomous agent.

## Constants
- `SIMULATION_START_TIME`: The start time of the simulation in minutes (9:00 AM).
- `SIMULATION_END_DAYS`: Number of days for the simulation (7 days).
- `ROOMS`: A list of rooms in the facility.
- `MESSAGE_THRESHOLD`: Number of coffees after which a stronger message is displayed.

## User Class
### Attributes
- `user_id`: Identifier for each user.
- `sleep_pattern`: Sleep pattern of the user (not explicitly used in the simulation).
- `heart_rate`: Initial heart rate of the user.
- `current_room`: The room where the user is currently located.
- `case_id`: Identifier for each case (day) of user activity.
- `last_day`: The last day the user was active.

### Methods
- `start_new_case()`: Initializes a new case (day) for the user.
- `move_between_rooms()`: Simulates user movement between rooms, recording events.
- `coffee_consumption()`: Simulates coffee consumption and its effects on heart rate.
- `respond_to_message()`: Simulates the user's response to messages.

## AutonomousAgent Class
### Attributes
- `users`: List of users being monitored.

### Methods
- `monitor_users()`: Monitors users and sends messages based on their heart rates.

## CoffeeMachine Class
### Attributes
- `users`: List of users.

### Methods
- `display_message()`: Displays messages to users and records corresponding events.

## Simulation Environment
- `env`: SimPy environment.

## Simulation Execution
- Users, coffee machine, and an autonomous agent are created.
- Processes for user movement, coffee consumption, and agent monitoring are initiated in the simulation environment.
- The simulation runs for the specified number of days.
- User activity events are recorded in a CSV file.
- The plot visualizes user movement over time.

## Visualization
- A plot is generated to visualize user activity over time.

## Output
- The resulting CSV file (`user_activity_log.csv`) contains recorded events.
- A plot (`user_activity_simulation.png`) visualizes user activity.

This code provides a flexible framework for simulating user activities in a facility over multiple days, capturing events such as room changes, coffee consumption, and responses to messages.
