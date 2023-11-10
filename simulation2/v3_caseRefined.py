import simpy
import matplotlib.pyplot as plt
import random
import csv
from datetime import datetime, timedelta

# Constants
SIMULATION_START_TIME = 9 * 60  # Start at 9:00 AM in minutes
SIMULATION_END_DAYS = 7  # Number of days for the simulation

SIMULATION_START_HOUR = 9  # Start at 9:00 AM
SIMULATION_END_HOUR = 18  # End at 6:00 PM
SIMULATION_DAYS = 30  # Number of simulation days
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
        self.case_id = 0  # Initialize case ID
        
    def start_new_case(self):
        self.case_id += 1  # Increment case ID for a new day
        

    def move_between_rooms(self):
        while True:
            # Generate random time for the user's stay in the room (between 15 to 45 minutes)
            stay_duration = random.randint(15, 45)

            # Choose a random room to move to
            next_room = random.choice(ROOMS)

            # Record the timestamp and room change event
            timestamp = datetime.fromtimestamp(env.now * 60).isoformat()
            event = {
                "Timestamp": timestamp,
                "User ID": self.user_id,
                "Case ID": f"Case-{self.user_id}-{self.case_id}",  # Include Case ID in the event log
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
                    "Case ID": self.case_id,  # Include Case ID in the event log
                    "Activity": "Take coffee"
                }
                write_event_to_csv(event)
                # Record the increased heart rate event
                timestamp = datetime.fromtimestamp(env.now * 60)
                event = {
                    "Timestamp": timestamp,
                    "User ID": self.user_id,
                    "Case ID": self.case_id,  # Include Case ID in the event log
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
                    "Case ID": self.case_id,  # Include Case ID in the event log
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
                        "Case ID": self.case_id,  # Include Case ID in the event log
                        "Activity": "Take coffee"
                    }
                    write_event_to_csv(event)
                    # Record the increased heart rate event
                    timestamp = datetime.fromtimestamp(env.now * 60)
                    event = {
                        "Timestamp": timestamp,
                        "User ID": self.user_id,
                        "Case ID": self.case_id,  # Include Case ID in the event log
                        "Activity": "Increased heart rate"
                    }
                    write_event_to_csv(event)

    def receive_message(self, message):
        # Simulate the user receiving a message
        timestamp = datetime.fromtimestamp(env.now * 60)
        event = {
            "Timestamp": timestamp,
            "User ID": self.user_id,
            "Case ID": self.case_id,  # Include Case ID in the event log
            "Activity": message
        }
        write_event_to_csv(event)
        # Simulate user's response to the message
        self.respond_to_message(message)

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
                        message = "Strong advice: Drink water now!"
                        self.coffee_machine.display_message(user.user_id, message)
                        # Record the message event in the case
                        user.receive_message(message)
                    else:
                        # Send a casual message to drink water
                        message = "Casual advice: Drink water now!"
                        self.coffee_machine.display_message(user.user_id, message)
                        # Record the message event in the case
                        user.receive_message(message)
            yield env.timeout(60)  # Check every minute

# Coffee Machine class
# Coffee Machine class
class CoffeeMachine:
    def __init__(self, env, users):
        self.env = env
        self.users = users  # Include users attribute in CoffeeMachine

    def display_message(self, user_id, message):
        # Display the message to the user
        timestamp = datetime.now().isoformat()

        event = {
            "Timestamp": timestamp,
            "User ID": user_id,
            "Case ID": self.users[0].case_id,  # Include Case ID in the event log
            "Activity": message
        }
        write_event_to_csv(event)
        # Simulate user's response to the message
        for user in self.users:  # Use self.users to access the users attribute
            if user.user_id == user_id:
                user.respond_to_message(message)


def write_event_to_csv(event):
    with open("user_activity_log.csv", mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "User ID", "Case ID", "Activity"])

        # Add a line to write headers if the file is empty
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(event)

# Simulation environment
env = simpy.Environment()

# Create users, coffee machine, and AI agent
users = [User(env, f"User-{i+1}", random.choice(["Good", "Bad"]), random.randint(60, 100)) for i in range(5)]
coffee_machine = CoffeeMachine(env, users)
agent = AutonomousAgent(env, users, coffee_machine)

# Start users' movement, coffee consumption, and AI agent monitoring

for user in users:
    user.start_new_case()  # Start a new case for each user
    env.process(user.move_between_rooms())
    env.process(user.coffee_consumption())

# Set up the plot for visualization
plt.figure(figsize=(10, 4))
plt.title("User Activity Simulation")
plt.xlabel("Time (minutes)")
plt.ylabel("Room")
plt.xticks(
    range(SIMULATION_START_HOUR * 60, SIMULATION_END_HOUR * 60 + 1, 60 * 30),  # Set ticks every 30 minutes
    [f"{i // 60:02d}:{i % 60:02d}" for i in range(SIMULATION_START_HOUR * 60, SIMULATION_END_HOUR * 60 + 1, 60 * 30)]
)
plt.yticks(range(len(ROOMS)), ROOMS)

# Start the simulation for each day
for day in range(SIMULATION_DAYS):
    # Set the case ID for each user at the beginning of the day
    for user in users:
        user.case_id = f"Case-{user.user_id}-{day + 1}"

    # Start the simulation for the day
    # Start the simulation for the specified number of days
env.run(until=(SIMULATION_START_TIME + SIMULATION_END_DAYS * 24 * 60)) 

# Save the plot
plt.savefig("user_activity_simulation.png")
plt.show()
