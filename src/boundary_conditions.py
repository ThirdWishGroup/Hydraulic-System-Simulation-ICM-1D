# src/boundary_conditions.py

from typing import Dict
from src.models import Node, OpenChannel
from src.solver import HydraulicSystem

def apply_boundary_conditions(system: 'HydraulicSystem') -> None:
    """
    Applies boundary conditions to the hydraulic system's nodes.
    """
    for node_id, node in system.nodes.items():
        if node.boundary_condition == 'Inflow' and node.inflow is not None:
            node.flow.Q = node.inflow
            # Assuming a rectangular channel for OpenChannel
            if isinstance(node.flow, OpenChannel):
                node.flow.A = node.flow.b * node.flow.h
        elif node.boundary_condition == 'Outflow' and node.outflow is not None:
            node.flow.Q = node.outflow
            # Assuming a rectangular channel for OpenChannel
            if isinstance(node.flow, OpenChannel):
                node.flow.A = node.flow.b * node.flow.h
