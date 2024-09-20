# src/visualization.py

import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict

def plot_flow_rate(df: pd.DataFrame) -> go.Figure:
    """
    Plots the flow rate over space for each node at the final time step.
    """
    # Extract the final time step
    final_time = df['Time'].max()
    df_final = df[df['Time'] == final_time]
    
    fig = go.Figure()
    for _, row in df_final.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['x']],
            y=[row["Flow Rate (Q)"]],
            mode='markers',
            name=f'Node {row["Node"]} Q'
        ))
    
    fig.update_layout(
        title=f"Flow Rate at Final Time Step (t = {final_time:.2f} s)",
        xaxis_title="Distance (m)",
        yaxis_title="Flow Rate (Q) [m³/s]",
        showlegend=True
    )
    return fig

def plot_hydraulic_head(df: pd.DataFrame) -> go.Figure:
    """
    Plots the hydraulic head over space for each node at the final time step.
    """
    # Extract the final time step
    final_time = df['Time'].max()
    df_final = df[df['Time'] == final_time]
    
    fig = go.Figure()
    for _, row in df_final.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['x']],
            y=[row["Depth (h)"]],
            mode='markers',
            name=f'Node {row["Node"]} h'
        ))
    
    fig.update_layout(
        title=f"Hydraulic Head at Final Time Step (t = {final_time:.2f} s)",
        xaxis_title="Distance (m)",
        yaxis_title="Hydraulic Head (h) [m]",
        showlegend=True
    )
    return fig

def plot_cross_sectional_area(df: pd.DataFrame) -> go.Figure:
    """
    Plots the cross-sectional area over space for each node at the final time step.
    """
    # Extract the final time step
    final_time = df['Time'].max()
    df_final = df[df['Time'] == final_time]
    
    fig = go.Figure()
    for _, row in df_final.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['x']],
            y=[row["Area (A)"]],
            mode='markers',
            name=f'Node {row["Node"]} A'
        ))
    
    fig.update_layout(
        title=f"Cross-Sectional Area at Final Time Step (t = {final_time:.2f} s)",
        xaxis_title="Distance (m)",
        yaxis_title="Cross-Sectional Area (A) [m²]",
        showlegend=True
    )
    return fig

def plot_free_surface_width(df: pd.DataFrame) -> go.Figure:
    """
    Plots the free surface width B for pressurized pipes at the final time step.
    (Assuming 'B' is included in the DataFrame)
    """
    # Extract the final time step
    final_time = df['Time'].max()
    df_final = df[df['Time'] == final_time]
    
    fig = go.Figure()
    for _, row in df_final.iterrows():
        if 'B' in row:
            fig.add_trace(go.Scatter(
                x=[row['x']],
                y=[row["B"]],
                mode='markers',
                name=f'Node {row["Node"]} B'
            ))
    
    fig.update_layout(
        title=f"Free Surface Width (B) at Final Time Step (t = {final_time:.2f} s)",
        xaxis_title="Distance (m)",
        yaxis_title="Free Surface Width (B) [m]",
        showlegend=True
    )
    return fig
