# src/utilities.py

from typing import Dict, Tuple
from src.models import Node, Flow, OpenChannel, PressurizedPipe
from src.constants import G

def validate_flow(flow: Flow) -> bool:
    """
    Validates that the flow rate and cross-sectional area are non-negative.
    """
    return flow.Q >= 0 and flow.A > 0 and flow.h >= 0

def validate_parameters(parameters: Dict, channel_type: str) -> Tuple[bool, str]:
    """
    Validates all input parameters to ensure they are physically meaningful.

    Args:
        parameters (Dict): Dictionary of parameters to validate.
        channel_type (str): Type of channel ('OpenChannel' or 'PressurizedPipe').

    Returns:
        Tuple[bool, str]: Tuple indicating validation status and error message.
    """
    for key, value in parameters.items():
        if value is None:
            # Only check for None if the parameter is required for the channel type
            if channel_type == 'PressurizedPipe' and key in ['Af', 'Cp']:
                return False, f"Parameter {key} must not be None."
            if channel_type == 'OpenChannel' and key in ['b', 'S0', 'n']:
                return False, f"Parameter {key} must not be None."
            continue  # Skip parameters not required for the selected channel type
        if key in ['Q', 'A', 'Af', 'Cp', 'delta_t', 'delta_x', 'S0', 'K', 'B', 'beta', 'slot_area']:
            if value < 0:
                return False, f"Parameter {key} must be non-negative."
        if key == 'theta' and not (0 < value <= 1):
            return False, "Parameter theta must be between 0 and 1 (exclusive of 0)."
    return True, ""

def initialize_nodes(num_nodes: int, channel_type: str = 'OpenChannel', h0: float = 2.0, u0: float = 0.0, b: float = 5.0, S0: float = 0.001, n: float = 0.03) -> Dict[int, Node]:
    """
    Initializes nodes with default Flow values based on channel type.

    Args:
        num_nodes (int): Number of nodes to initialize.
        channel_type (str): Type of channel ('OpenChannel' or 'PressurizedPipe').
        h0 (float): Initial depth.
        u0 (float): Initial velocity.
        b (float): Channel width (for OpenChannel).
        S0 (float): Bed slope.
        n (float): Manning's roughness coefficient.

    Returns:
        Dict[int, Node]: Dictionary of initialized nodes.
    """
    nodes = {}
    for i in range(num_nodes):
        if channel_type == 'OpenChannel':
            A = b * h0  # Cross-sectional area
            Q = A * u0  # Flow rate (m³/s)
            flow = OpenChannel(
                Q=Q,
                A=A,
                h=h0,
                b=b,
                theta=0.0,
                S0=S0,
                K=50.0,
                n=n
            )
            nodes[i] = Node(id=i, flow=flow)
        elif channel_type == 'PressurizedPipe':
            # Implement PressurizedPipe initialization if needed
            # Placeholder implementation
            Af = 5.0  # Full cross-sectional area
            Cp = 1000.0  # Pressure wave speed
            B = compute_free_surface_width(Af, Cp)
            A = Af  # Assume pipe is initially full
            Q = 20.0  # Flow rate (m³/s)
            flow = PressurizedPipe(
                Q=Q,
                A=A,
                h=h0,
                Af=Af,
                Cp=Cp,
                B=B
            )
            nodes[i] = Node(id=i, flow=flow)
    return nodes

def add_connection(beta: Dict[int, Dict[int, float]], from_node: int, to_node: int, beta_val: float) -> None:
    """
    Adds a connection between two nodes with a weighting coefficient.

    Args:
        beta (Dict[int, Dict[int, float]]): Dictionary representing connections.
        from_node (int): Source node ID.
        to_node (int): Destination node ID.
        beta_val (float): Weighting coefficient.
    """
    if from_node in beta:
        beta[from_node][to_node] = beta_val
    else:
        beta[from_node] = {to_node: beta_val}

def compute_free_surface_width(Af: float, Cp: float, G: float = 9.81) -> float:
    """
    Computes the free surface width B in pressurized pipes.

    Args:
        Af (float): Full cross-sectional area (m²).
        Cp (float): Pressure wave speed (m/s).
        G (float): Acceleration due to gravity (m/s²).

    Returns:
        float: Free surface width B (m).
    """
    return (G * Af) / (Cp ** 2)

def check_cfl_condition(Cp: float, delta_t: float, delta_x: float, cfl_max: float = 1.0) -> bool:
    """
    Checks if the CFL condition is satisfied.

    Args:
        Cp (float): Pressure wave speed (m/s).
        delta_t (float): Time step size (s).
        delta_x (float): Spatial step size (m).
        cfl_max (float): Maximum allowable CFL number.

    Returns:
        bool: True if CFL condition is satisfied, False otherwise.
    """
    if Cp <= 0 or delta_x <= 0:
        return False
    cfl = (Cp * delta_t) / delta_x
    return cfl <= cfl_max
