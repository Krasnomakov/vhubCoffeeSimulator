#This script generates simulation and data for eventlog. 
#users move around three zones in the vitality Hub
#certain rules are aplied 
#users can only take coffee after they got to coffee area 
#when they get coffee their heart rate increases 
#after 2 pm users start receiving messages nudging them to drink water 
#users can either accept message and take water or get another coffee
#simulation starts and ends within one day timeframe

import simpy
import matplotlib.pyplot as plt
import random
import csv
from datetime import datetime

# Constants
SIMULATION_START_TIME = 9 * 60  # Start at 9:00 AM in minutes
SIMULATION_END_TIME = 18 * 60  # End at 6:00 PM in minutes
ROOMS = ["Workplace", "Meeting Room", "Coffee Area"]
MESSAGE_THRESHOLD = 2  # Number of coffees after which a stronger message is displayed

# User class
class User:
    def __init__(self, env, user_id, sleep_pattern, initial_heart_rate):
        self.env = env
        self.user_id = user_id
        self.sleep_pattern = sleep_pattern
        self.heart_rate = initial_heart_rate
        self.current_room = None  # Track the user's current room

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

            # Update the current room
            self.current_room = next_room

            # Visualize the user's movement on the plot
            plt.scatter(env.now, ROOMS.index(next_room), c='b', label=self.user_id, marker='o')
            plt.pause(0.1)

            # Simulate the user's stay in the room
            yield env.timeout(stay_duration)

    def coffee_consumption(self):
        while True:
            # Simulate coffee consumption when the user is in the "Coffee Area"
            if self.current_room == "Coffee Area" and random.random() < 0.2:
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

    def respond_to_message(self, message):
        if message.startswith("Strong advice: Drink water"):
            # Simulate user's response to a strong message
            if random.random() < 0.7:  # Probability of taking water
                self.heart_rate -= 5  # Decrease heart rate when drinking water
                # Record the water consumption event
                timestamp = datetime.fromtimestamp(env.now * 60)
                event = {
                    "Timestamp": timestamp,
                    "User ID": self.user_id,
                    "Activity": "Take water"
                }
                write_event_to_csv(event)
            else:
                # User ignores the message and takes another coffee
                if self.current_room == "Coffee Area" and random.random() < 0.2:
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

# AI Autonomous Agent class
class AutonomousAgent:
    def __init__(self, env, users, coffee_machine):
        self.env = env
        self.users = users
        self.coffee_machine = coffee_machine

    def monitor_users(self):
        while True:
            # Check if it's after 2 PM
            if env.now >= 14 * 60:
                for user in self.users:
                    if user.heart_rate > MESSAGE_THRESHOLD:
                        # Send a strong message to drink water
                        self.coffee_machine.display_message(user.user_id, "Strong advice: Drink water now!")
                    else:
                        # Send a casual message to drink water
                        self.coffee_machine.display_message(user.user_id, "Casual advice: Drink water now!")
            yield env.timeout(60)  # Check every minute

# Coffee Machine class
class CoffeeMachine:
    def __init__(self, env):
        self.env = env

    def display_message(self, user_id, message):
        # Display the message to the user
        timestamp = datetime.now().isoformat()

        event = {
            "Timestamp": timestamp,
            "User ID": user_id,
            "Activity": message
        }
        write_event_to_csv(event)
        # Simulate user's response to the message
        for user in users:
            if user.user_id == user_id:
                user.respond_to_message(message)

def write_event_to_csv(event):
    with open("user_activity_log.csv", mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "User ID", "Activity"])
        writer.writerow(event)


# Simulation environment
env = simpy.Environment()

# Create users, coffee machine, and AI agent
users = [User(env, f"User-{i+1}", random.choice(["Good", "Bad"]), random.randint(60, 100)) for i in range(5)]
coffee_machine = CoffeeMachine(env)
agent = AutonomousAgent(env, users, coffee_machine)

# Start users' movement, coffee consumption, and AI agent monitoring
for user in users:
    env.process(user.move_between_rooms())
    env.process(user.coffee_consumption())
env.process(agent.monitor_users())

# Set up the plot for visualization
plt.figure(figsize=(10, 4))
plt.title("User Activity Simulation")
plt.xlabel("Time (minutes)")
plt.ylabel("Room")
plt.xticks(
    range(SIMULATION_START_TIME, SIMULATION_END_TIME + 1, 60 * 30),  # Set ticks every 30 minutes
    [f"{i // 60:02d}:{i % 60:02d}" for i in range(SIMULATION_START_TIME, SIMULATION_END_TIME + 1, 60 * 30)]
)
plt.yticks(range(len(ROOMS)), ROOMS)

# Start the simulation
env.run(until=SIMULATION_END_TIME)

# Save the plot
plt.savefig("user_activity_simulation.png")
plt.show()
