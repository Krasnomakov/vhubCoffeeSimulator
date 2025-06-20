# Simulation 2

This folder contains the final, refined versions of the VHUB user simulation. The primary goal of these scripts is to generate a clean, case-based event log suitable for process mining.

The main script in this folder is **`v4_simulationWithCases.py`**.

## Final Simulation: `v4_simulationWithCases.py`

This script simulates user activity in an office environment over several days. It is designed to be a flexible framework for generating event logs.

### Key Features:

*   **Multi-Day Simulation:** The simulation runs continuously for a specified number of days (`SIMULATION_END_DAYS`).
*   **Case IDs:** Each user's activity for a given day is assigned a unique `Case ID` (e.g., `Case-User-1-1`), which is essential for process mining. This is handled automatically as the simulation crosses into a new day.
*   **User Behavior:** Users move between rooms, consume coffee (which increases their heart rate), and respond to messages from an AI agent.
*   **AI Agent:** An autonomous agent monitors users and sends them messages to drink water based on their heart rate.
*   **Event Logging:** All activities are logged to `user_activity_log.csv` with a timestamp, user ID, case ID, and activity description.
*   **Visualization:** A plot is generated (`user_activity_simulation.png`) to visualize user movement over time. 