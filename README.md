# VHUB Coffee Simulator

This repository contains a Python-based simulation of user behavior in an office environment, designed to generate event logs for process mining.

## Project Structure

-   `/simulation1`: Contains the initial, exploratory development iterations.
-   `/simulation2`: Contains the final, refined simulation scripts.

**The final and main script for this project is [`/simulation2/v4_simulationWithCases.py`](./simulation2/v4_simulationWithCases.py).**

**Demo:** https://vimeo.com/883906069/c506d45580

## Final Simulation Overview

The final simulation (`v4_simulationWithCases.py`) models the daily activities of users within a facility over multiple days. It captures events such as room changes, coffee consumption, and responses to AI-driven messages, logging everything into a CSV file with unique case IDs for each user-day.

### Core Components

-   **User:** Represents an individual in the simulation, tracking their location, heart rate, and daily activity case.
-   **AutonomousAgent:** Monitors users and sends messages to encourage healthy behavior (e.g., drinking water).
-   **CoffeeMachine:** Acts as an interface for the agent to deliver messages to the users.
-   **Simulation Environment:** A `simpy` environment that manages the simulation clock and events.

### Output

-   `user_activity_log.csv`: A structured event log file.
-   `user_activity_simulation.png`: A plot visualizing user movements over time.
