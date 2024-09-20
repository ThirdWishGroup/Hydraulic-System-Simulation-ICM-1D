# streamlit_app.py

import streamlit as st
import numpy as np
import pandas as pd
from src.constants import G
from src.models import OpenChannel, PressurizedPipe, Node
from src.solver import HydraulicSystem
from src.utilities import (
    validate_parameters, initialize_nodes, add_connection,
    compute_free_surface_width, check_cfl_condition
)
from src.visualization import (
    plot_flow_rate, plot_hydraulic_head,
    plot_cross_sectional_area, plot_free_surface_width
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Hydraulic System Simulation ICM 1D")

    st.sidebar.header("Simulation Parameters")

    # Initialize parameters within valid ranges
    num_nodes = st.sidebar.number_input("Number of Nodes", min_value=2, max_value=1000, value=100, step=1)
    delta_x = st.sidebar.number_input("Spatial Step Size (Δx) [m]", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
    total_time = st.sidebar.number_input("Total Simulation Time [s]", min_value=0.1, max_value=10000.0, value=200.0, step=0.1)
    CFL = st.sidebar.slider("CFL Number", 0.1, 1.0, 0.9, step=0.1)

    st.sidebar.header("Channel Geometry")
    channel_type = st.sidebar.selectbox("Select Channel Type", ["OpenChannel"])  # Solver implemented for OpenChannel

    # Set initial parameters
    b = st.sidebar.number_input("Channel Width (b) [m]", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    S0 = st.sidebar.number_input("Bed Slope (S0)", min_value=0.0, max_value=0.1, value=0.001, step=0.0001)
    n_manning = st.sidebar.number_input("Manning's Roughness Coefficient (n)", min_value=0.01, max_value=0.1, value=0.03, step=0.001)

    # Boundary Conditions setup
    st.sidebar.header("Boundary Conditions")
    h_in = st.sidebar.number_input("Upstream Depth (h_in) [m]", min_value=0.1, max_value=50.0, value=2.0, step=0.1)
    u_in = st.sidebar.number_input("Upstream Velocity (u_in) [m/s]", min_value=0.0, max_value=50.0, value=2.0, step=0.1)
    h_out = st.sidebar.number_input("Downstream Depth (h_out) [m]", min_value=0.1, max_value=50.0, value=2.0, step=0.1)

    # Initial conditions
    h0 = st.sidebar.number_input("Initial Depth (h0) [m]", min_value=0.1, max_value=50.0, value=2.0, step=0.1)
    u0 = st.sidebar.number_input("Initial Velocity (u0) [m/s]", min_value=0.0, max_value=50.0, value=0.0, step=0.1)

    # Validate parameters
    params = {
        "delta_x": delta_x,
        "total_time": total_time,
        "CFL": CFL,
        "b": b,
        "S0": S0,
        "n": n_manning,
        "h_in": h_in,
        "u_in": u_in,
        "h_out": h_out,
        "h0": h0,
        "u0": u0
    }

    valid_params, error_msg = validate_parameters(params, channel_type)
    if not valid_params:
        st.error(f"Invalid input parameters: {error_msg}")
        st.stop()

    # Initialize nodes with the proper geometry type
    nodes = initialize_nodes(
        int(num_nodes),
        channel_type=channel_type,
        h0=h0,
        u0=u0,
        b=b,
        S0=S0,
        n=n_manning
    )

    # Create HydraulicSystem instance
    system = HydraulicSystem(
        nodes=nodes,
        delta_x=delta_x,
        total_time=total_time,
        CFL=CFL,
        h_in=h_in,
        u_in=u_in,
        h_out=h_out
    )

    # Check CFL condition and notify the user if violated
    cfl_condition_met = True
    if channel_type == "OpenChannel":
        # Estimate maximum wave speed
        max_velocity = max((node.flow.Q / node.flow.A) if node.flow.A > 0 else 0.0 for node in nodes.values())
        max_depth = max(node.flow.h for node in nodes.values())
        c = np.sqrt(G * max_depth)
        max_wave_speed = max_velocity + c
        cfl = CFL  # Since CFL = max_speed * dt / dx = 0.9, and dt is dynamically set
        if cfl >= 1:
            cfl_condition_met = False
            st.error(f"CFL condition not satisfied (CFL={cfl:.2f}). Adjust Δx or CFL number.")
    elif channel_type == "PressurizedPipe":
        # Add CFL condition check for PressurizedPipe if implemented
        pass  # Currently only handling OpenChannel

    # Disable simulation button if conditions are not met
    if not cfl_condition_met:
        st.error("Simulation cannot proceed due to unsatisfied CFL condition.")
    else:
        if st.button("Run Simulation"):
            # Run simulation
            try:
                # Run simulation using the updated solver
                results, x = system.run_simulation()

                # Convert results to DataFrame
                df_results = pd.DataFrame(results)
                st.success("Simulation completed successfully!")
                st.dataframe(df_results)

                # Visualization
                st.subheader("Flow Rate Over Distance")
                flow_fig = plot_flow_rate(df_results)
                st.plotly_chart(flow_fig)

                st.subheader("Depth Over Distance")
                depth_fig = plot_hydraulic_head(df_results)
                st.plotly_chart(depth_fig)

                st.subheader("Cross-Sectional Area Over Distance")
                area_fig = plot_cross_sectional_area(df_results)
                st.plotly_chart(area_fig)

                # If using free surface width for PressurizedPipe
                if channel_type == "PressurizedPipe":
                    st.subheader("Free Surface Width Over Distance")
                    # Assuming 'B' is part of the Node flow attributes
                    # Add 'B' to results in run_simulation if not already present
                    # Here, it's not included, so you might need to adjust your solver
                    pass

            except Exception as e:
                st.error(f"An error occurred during simulation: {e}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by Third Wish Group")

if __name__ == "__main__":
    main()
