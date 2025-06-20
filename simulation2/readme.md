# ✨ Simulation 2: Final Version

This folder contains the final, refined versions of the VHUB user simulation. The primary goal of these scripts is to generate a clean, case-based event log suitable for process mining.

The main script in this folder is **`v4_simulationWithCases.py`**.

---

### 🚀 Final Simulation: `v4_simulationWithCases.py`

This script simulates user activity in an office environment over several days. It is designed as a flexible framework for generating event logs, built with the following technologies:

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Simpy](https://img.shields.io/badge/Simpy-4E9A06?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=matplotlib&logoColor=white)

### 🌟 Key Features:

-   **🗓️ Multi-Day Simulation:** Runs continuously for a specified number of days (`SIMULATION_END_DAYS`).
-   **🆔 Case IDs:** Assigns a unique `Case ID` (e.g., `Case-User-1-1`) for each user's daily activity, which is essential for process mining.
-   **🚶 User Behavior:** Models users moving between rooms, consuming coffee (which increases their heart rate), and responding to messages from an AI agent.
-   **🤖 AI Agent:** An autonomous agent monitors users and sends them messages to drink water based on their heart rate.
-   **✍️ Event Logging:** All activities are logged to `user_activity_log.csv` with a timestamp, user ID, case ID, and activity description.
-   **📊 Visualization:** Generates a plot (`user_activity_simulation.png`) to visualize user movement over time. 