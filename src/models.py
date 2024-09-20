# src/models.py

from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Flow:
    Q: float  # Flow rate (m³/s)
    A: float  # Cross-sectional area (m²)
    h: float  # Hydraulic head (m)

    def __post_init__(self):
        self.Q_prev = self.Q
        self.A_prev = self.A

@dataclass
class OpenChannel(Flow):
    b: float      # Channel width (m)
    theta: float  # Bed slope angle (radians)
    S0: float     # Bed slope (dimensionless)
    K: float      # Conveyance (m^(1/3)/s)
    n: float      # Manning's roughness coefficient

@dataclass
class PressurizedPipe(Flow):
    Af: float     # Full cross-sectional area (m²)
    Cp: float     # Speed of pressure wave (m/s)
    B: float      # Free surface width (m)

@dataclass
class Node:
    id: int
    flow: Flow
    boundary_condition: Optional[str] = None  # 'Inflow', 'Outflow', or None
    inflow: Optional[float] = None           # Inflow rate (m³/s) if boundary condition is Inflow
    outflow: Optional[float] = None          # Outflow rate (m³/s) if boundary condition is Outflow
    connections: Dict[int, float] = field(default_factory=dict)  # Connected node IDs with beta coefficients
