#An attempt to set proper rules execution and shape the behaviour

import simpy
import matplotlib.pyplot as plt
import random
import csv
from datetime import datetime

# Constants
SIMULATION_START_TIME = 9 * 60  # Start at 9:00 AM in minutes
SIMULATION_END_TIME = 18 * 60  # End at 6:00 PM in minutes
ROOMS = ["Entrance", "Workplace", "Meeting Room", "Coffee Area"]
MESSAGE_THRESHOLD = 2  # Number of coffees after which a stronger message is displayed

# User class
class User:
    def __init__(self, env, user_id, sleep_pattern, initial_heart_rate):
        self.env = env
        self.user_id = user_id
        self.sleep_pattern = sleep_pattern
        self.heart_rate = initial_heart_rate

    def move_between_rooms(self):
        # Ensure users start at the entrance with a normal heart rate
        if self.env.now == SIMULATION_START_TIME:
            self.heart_rate = random.randint(60, 100)

        yield env.timeout(0)
        while True:
            # Generate random time for the user's stay in the room (between 15 to 45 minutes)
            stay_duration = random.randint(15, 45)

            # Choose a random room to move to (except the entrance at the end of the day)
            next_room = random.choice(ROOMS[1:])

            # Record the timestamp and room change event
            timestamp = datetime.fromtimestamp(env.now * 60)
            event = {
                "Timestamp": timestamp,
                "User ID": self.user_id,
                "Activity": f"Move to {next_room}"
            }
            write_event_to_csv(event)

            # Update the current room
            self.set_current_room(next_room)

            # Visualize the user's movement on the plot
            plt.scatter(env.now, ROOMS.index(next_room), c='b', label=self.user_id, marker='o')
            plt.pause(0.1)

            # Simulate the user's stay in the room
            yield env.timeout(stay_duration)

    def coffee_consumption(self):
        while True:
            if self.env.now >= SIMULATION_START_TIME:
                if self.current_room == "Coffee Area":
                    if random.random() < 0.2:
                        self.heart_rate += 5
                        # Record the coffee consumption event
                        timestamp = datetime.fromtimestamp(env.now * 60)
                        event = {
                            "Timestamp": timestamp,
                            "User ID": self.user_id,
                            "Activity": "Take coffee"
                        }
                        write_event_to_csv(event)
                else:
                    self.heart_rate += 5  # Increased heart rate for being in a different room
            rest_duration = random.randint(30, 90)
            yield env.timeout(rest_duration)
            
    def set_current_room(self, room):
        self.current_room = room
        
    def drink_water(self):
        self.heart_rate -= 3  # Drinking water reduces heart rate
        timestamp = datetime.fromtimestamp(env.now * 60)
        event = {
            "Timestamp": timestamp,
            "User ID": self.user_id,
            "Activity": "User took water"
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
            if env.now >= SIMULATION_START_TIME + 5 * 60:
                for user in self.users:
                    if user.heart_rate > MESSAGE_THRESHOLD:
                        if user.current_room == "Coffee Area":
                            response = random.choice(["Accept", "Ignore"])
                            if response == "Accept":
                                self.coffee_machine.display_message(user.user_id, "User, it's time to drink water.")  # Message recommending water
                                # Check if a "Recommend water" event was already recorded for this user
                                if not user.water_recommendation_given:
                                    user.water_recommendation_given = True  # Mark that the recommendation was given
                                    # Record the "Recommend water" event
                                    timestamp = datetime.fromtimestamp(env.now * 60)
                                    event = {
                                        "Timestamp": timestamp,
                                        "User ID": user.user_id,
                                        "Activity": "Recommend water"
                                    }
                                    write_event_to_csv(event)
                            else:
                                self.coffee_machine.display_message(user.user_id, "User took another coffee")
                                user.heart_rate += 5
                    else:
                        if user.current_room == "Coffee Area":
                            response = random.choice(["Accept", "Ignore"])
                            if response == "Accept":
                                self.coffee_machine.display_message(user.user_id, "User, it's time to drink water.")  # Message recommending water
                                # Check if a "Recommend water" event was already recorded for this user
                                if not user.water_recommendation_given:
                                    user.water_recommendation_given = True  # Mark that the recommendation was given
                                    # Record the "Recommend water" event
                                    timestamp = datetime.fromtimestamp(env.now * 60)
                                    event = {
                                        "Timestamp": timestamp,
                                        "User ID": user.user_id,
                                        "Activity": "Recommend water"
                                    }
                                    write_event_to_csv(event)
                                else:
                                    self.coffee_machine.display_message(user.user_id, "User took another coffee")
                                    user.heart_rate += 5
            yield env.timeout(60)


# Coffee Machine class
class CoffeeMachine:
    def __init__(self, env):
        self.env = env

    def display_message(self, user_id, message):
        # Display the message to the user
        timestamp = datetime.fromtimestamp(env.now * 60)
        event = {
            "Timestamp": timestamp,
            "User ID": user_id,
            "Activity": message
        }
        write_event_to_csv(event)
        
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
    range(SIMULATION_START_TIME, SIMULATION_END_TIME+1, 60*30),  # Set ticks every 30 minutes
    [f"{i // 60:02d}:{i % 60:02d}" for i in range(SIMULATION_START_TIME, SIMULATION_END_TIME+1, 60*30)]
)
plt.yticks(range(len(ROOMS)), ROOMS)

# Start the simulation
env.run(until=SIMULATION_END_TIME)

# Save the plot
plt.savefig("user_activity_simulation.png")
plt.show()
