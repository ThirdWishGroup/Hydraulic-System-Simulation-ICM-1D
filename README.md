# Hydraulic System Simulation ICM 1D

This project is a Streamlit-based application for simulating a one-dimensional hydraulic system, primarily focusing on open channel flow. The simulation computes and visualizes key hydraulic parameters such as flow rate, hydraulic head (depth), and cross-sectional area over a defined spatial domain.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Simulation Details](#simulation-details)
- [Logging & Error Handling](#logging--error-handling)
- [Credits](#credits)

---

## Overview

The simulation tool is designed to provide an interactive environment where users can adjust simulation parameters, run a hydraulic simulation, and visualize the results in real time. The application uses a 1D model for hydraulic systems, initially supporting the **OpenChannel** type. It includes functionality for validating parameters, initializing simulation nodes, checking numerical stability through the CFL condition, and generating plots for analysis.

---

## Features

- **Interactive UI:** Powered by Streamlit, allowing users to set simulation parameters through an intuitive sidebar.
- **Parameter Validation:** Ensures that input values meet required constraints and notifies the user if the simulation cannot proceed.
- **Dynamic Simulation:** Implements a solver for hydraulic systems that computes the evolution of flow variables over time and space.
- **Visualization:** Generates interactive plots for:
  - Flow Rate vs. Distance
  - Hydraulic Head (Depth) vs. Distance
  - Cross-Sectional Area vs. Distance
  - (Future support for Free Surface Width visualization in pressurized pipe systems)
- **Logging:** Configured logging for debugging and tracking simulation progress.

---

1. **Install Dependencies:**

   Ensure you have Python 3.x installed. Then, install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   *The `requirements.txt` file should include:*
   - streamlit
   - numpy
   - pandas
   - plotly (if required by visualization functions)
   - Other dependencies as used in the project modules

---

## Usage

To launch the simulation app, run the following command in your terminal:

```bash
streamlit run streamlit_app.py
```

After running the command, a browser window will open displaying the simulation interface. Use the sidebar to configure simulation parameters such as:

- **Number of Nodes:** Determines the spatial resolution.
- **Spatial Step Size (Δx):** Defines the distance between nodes.
- **Total Simulation Time:** Sets the duration of the simulation.
- **CFL Number:** Controls the numerical stability condition.
- **Channel Geometry Parameters:** Width, bed slope, and Manning's roughness.
- **Boundary & Initial Conditions:** Upstream and downstream depths, velocities, and initial conditions.

Press the **Run Simulation** button to execute the simulation. Results will be presented in both tabular form and as interactive plots.

---

## Code Structure

- **`streamlit_app.py`**: Entry point of the application. Contains the Streamlit interface and simulation logic.
- **`src/constants.py`**: Defines global constants (e.g., gravitational constant `G`).
- **`src/models.py`**: Contains classes for hydraulic components like `OpenChannel`, `PressurizedPipe`, and `Node`.
- **`src/solver.py`**: Implements the `HydraulicSystem` class which contains the simulation engine.
- **`src/utilities.py`**: Provides helper functions for parameter validation, node initialization, adding connections, computing free surface width, and checking the CFL condition.
- **`src/visualization.py`**: Includes functions for generating plots of the simulation results.

---

## Simulation Details

- **Hydraulic System:** The simulation models an open channel flow where key parameters such as depth, velocity, and flow rate evolve along the channel.
- **CFL Condition:** The simulation checks the Courant–Friedrichs–Lewy (CFL) condition to ensure numerical stability. If the condition is violated, the simulation will not run until the parameters are adjusted.
- **Numerical Solver:** Utilizes a 1D solver that updates the hydraulic state of each node based on the input parameters and boundary conditions.

---

## Logging & Error Handling

- **Logging:** The application uses Python’s built-in logging module to record informational messages. Logs can help in debugging and tracking the simulation progress.
- **Error Handling:** Input parameters are validated before running the simulation. If invalid parameters are detected or if the CFL condition is not met, appropriate error messages are displayed to the user.

