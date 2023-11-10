#heart rate property is added into user class

import simpy
import matplotlib.pyplot as plt
import random
import csv
from datetime import datetime

# Constants
SIMULATION_START_TIME = 9 * 60  # Start at 9:00 AM in minutes
SIMULATION_END_TIME = 18 * 60  # End at 6:00 PM in minutes
ROOMS = ["Entrance", "Workplace", "Meeting Room", "Coffee Area"]

# User class
class User:
    def __init__(self, env, user_id, sleep_pattern, initial_heart_rate):
        self.env = env
        self.user_id = user_id
        self.sleep_pattern = sleep_pattern
        self.heart_rate = initial_heart_rate

    def move_between_rooms(self):
        while True:
            # Generate random time for the user's stay in the room (between 15 to 45 minutes)
            stay_duration = random.randint(15, 45)
            
            # Choose a random room to move to
            next_room = random.choice(ROOMS)
            
            # Record the timestamp and room change event
            timestamp = datetime.fromtimestamp(env.now * 60)
            event = {
                "Timestamp": timestamp,
                "User ID": self.user_id,
                "Activity": f"Move to {next_room}"
            }
            write_event_to_csv(event)
            
            # Visualize the user's movement on the plot
            plt.scatter(env.now, ROOMS.index(next_room), c='b', label=self.user_id, marker='o')
            plt.pause(0.1)
            
            # Simulate the user's stay in the room
            yield env.timeout(stay_duration)
    
    def coffee_consumption(self):
        while True:
            # Simulate coffee consumption
            if random.random() < 0.2:  # Randomly decide to take coffee (adjust as needed)
                self.heart_rate += 5  # Increase heart rate when coffee is consumed
                # Record the coffee consumption event
                timestamp = datetime.fromtimestamp(env.now * 60)
                event = {
                    "Timestamp": timestamp,
                    "User ID": self.user_id,
                    "Activity": "Take coffee"
                }
                write_event_to_csv(event)
                # Record the increased heart rate event
                timestamp = datetime.fromtimestamp(env.now * 60)
                event = {
                    "Timestamp": timestamp,
                    "User ID": self.user_id,
                    "Activity": "Increased heart rate"
                }
                write_event_to_csv(event)
            
            # Simulate user's rest (random time between 30 to 90 minutes)
            rest_duration = random.randint(30, 90)
            yield env.timeout(rest_duration)

def write_event_to_csv(event):
    with open("user_activity_log.csv", mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "User ID", "Activity"])
        writer.writerow(event)

# Simulation environment
env = simpy.Environment()

# Create users with initial variables
users = [User(env, f"User-{i+1}", random.choice(["Good", "Bad"]), random.randint(60, 100)) for i in range(5)]  # Create 5 users

# Start users' movement and coffee consumption
for user in users:
    env.process(user.move_between_rooms())
    env.process(user.coffee_consumption())

# Set up the plot for visualization
plt.figure(figsize=(10, 4))
plt.title("User Activity Simulation")
plt.xlabel("Time (minutes)")
plt.ylabel("Room")
plt.xticks(
    range(SIMULATION_START_TIME, SIMULATION_END_TIME+1, 60*30),  # Set ticks every 30 minutes
    [f"{i // 60:02d}:{i % 60:02d}" for i in range(SIMULATION_START_TIME, SIMULATION_END_TIME+1, 60*30)]
)
plt.yticks(range(len(ROOMS)), ROOMS)

# Start the simulation
env.run(until=SIMULATION_END_TIME)

# Save the plot
plt.savefig("user_activity_simulation.png")
plt.show()
