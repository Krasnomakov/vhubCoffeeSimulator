# VHUB User Simulation (simulation2)

This folder contains several iterations of a Python-based simulation for modeling user behavior in an office environment. The simulation is built using `simpy` and is designed to generate event logs for process mining analysis, possibly with Celonis.

The core purpose of the simulation is to model users moving between different rooms, performing actions like drinking coffee or water, and generating a structured event log with case IDs.

## Simulation Files

The folder contains several versions of the simulation script, each building upon the last.

*   `user_activity_log.csv`: A CSV file that logs all events during the simulation. This is the primary output.

### Simulation Script Evolution

Here is a detailed breakdown of each version of the Python script: 

| File Name                      | Key Features & Changes                                                                                                                                                             | Notable Bugs & Flaws                                                                                                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `v1_refinedForCelonis.py`      | - **Baseline:** A refined version combining the best features from `simulation1`.<br>- Includes context-aware actions and a `User` class that responds to messages.                   | - **Bug:** `MESSAGE_THRESHOLD` is `2` but is compared against heart rate (`>60`).<br>- Timestamp in `CoffeeMachine` uses `datetime.now()`, which is inconsistent with the simulation clock. |
| `v2_vHubSimulationWithCases.py` | - **Case IDs:** Adds a `Case ID` to the event log.<br>- **Multi-day:** Attempts to run the simulation for 30 days.                                                                   | - **Major Flaw:** The multi-day simulation logic is broken; the `simpy` environment is not reset each day, so it only runs for one day.                                           |
| `v3_caseRefined.py`            | - **Refactoring:** Attempts to refine case ID logic and multi-day simulation.<br>- Adds a `receive_message` method to the `User` class.                                               | - **Confusing:** The code is overly complex and contains redundant logic for time and cases.<br>- The multi-day logic is still flawed.                                              |
| `v4_simulationWithCases.py`    | - **Correct Cases:** Implements a much cleaner and more effective method for handling cases across a continuous multi-day simulation by checking the day number within the process. | - **Bug:** The `MESSAGE_THRESHOLD` logic bug persists.<br>- **Bug:** The `CoffeeMachine` still logs messages with an incorrect `Case ID`.                                              |

## Conclusion

This simulation series focuses on generating a structured event log suitable for process mining. The scripts evolve from a single-day simulation to a multi-day one with proper case identifiers.

**`v4_simulationWithCases.py`** is the most advanced and functional version in this folder. It provides a solid foundation for generating a multi-day event log with consistent case IDs for each user per day. While it still contains a persistent minor bug in the agent's message triggering logic and the coffee machine's logging, its core data generation capability is the most robust. 