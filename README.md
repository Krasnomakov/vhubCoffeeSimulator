# ☕ VHUB Coffee Simulator

This repository contains a Python-based simulation of user behavior in an office environment, designed to generate event logs for process mining.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Simpy](https://img.shields.io/badge/Simpy-4E9A06?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=matplotlib&logoColor=white)

---

## 🚀 Final Simulation

The final and main script for this project is **[`/simulation2/v4_simulationWithCases.py`](./simulation2/v4_simulationWithCases.py)**.

This simulation models the daily activities of users within a facility over multiple days. It captures events such as room changes, coffee consumption, and responses to AI-driven messages, logging everything into a CSV file with unique case IDs for each user-day.

**📹 Demo Video:** https://vimeo.com/883906069/c506d45580

---

## 📂 Project Structure

-   **`/simulation1`**: Contains the initial, exploratory development iterations. See the [local README](./simulation1/readme.md) for more details.
-   **`/simulation2`**: Contains the final, refined simulation scripts. See the [local README](./simulation2/readme.md) for a detailed breakdown.

---

## ⚙️ Core Components of the Final Simulation

-   **🧑‍💻 User:** Represents an individual in the simulation, tracking their location, heart rate, and daily activity case.
-   **🤖 AutonomousAgent:** Monitors users and sends messages to encourage healthy behavior (e.g., drinking water).
-   **☕ CoffeeMachine:** Acts as an interface for the agent to deliver messages to the users.
-   **⏰ Simulation Environment:** A `simpy` environment that manages the simulation clock and events.

## 📊 Output

-   **`user_activity_log.csv`**: A structured event log file.
-   **`user_activity_simulation.png`**: A plot visualizing user movements over time.
