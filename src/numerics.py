# src/numerics.py

import numpy as np
from typing import Dict
from src.models import Node, OpenChannel
from src.constants import G
import logging

logger = logging.getLogger(__name__)

def compute_flux(U):
    """
    Compute the physical flux for the given conserved variables U.
    """
    h = U[0]
    hu = U[1]
    u = hu / h if h > 0 else 0.0
    flux = np.array([hu, hu * u + 0.5 * G * h ** 2])
    return flux

def compute_source(U, S0, n):
    """
    Compute the source term for the given conserved variables U.
    """
    h = U[0]
    hu = U[1]
    u = hu / h if h > 0 else 0.0
    Sf = n ** 2 * u * abs(u) / (h ** (4 / 3)) if h > 0 else 0.0
    S = np.array([0.0, -G * h * (S0 + Sf)])
    return S

def hll_flux(U_left, U_right):
    """
    Compute the HLL numerical flux between two states.
    """
    # Left state
    h_L, hu_L = U_left
    u_L = hu_L / h_L if h_L > 0 else 0.0
    c_L = np.sqrt(G * h_L) if h_L > 0 else 0.0

    # Right state
    h_R, hu_R = U_right
    u_R = hu_R / h_R if h_R > 0 else 0.0
    c_R = np.sqrt(G * h_R) if h_R > 0 else 0.0

    # Compute wave speeds
    S_L = min(u_L - c_L, u_R - c_R)
    S_R = max(u_L + c_L, u_R + c_R)

    # Compute fluxes
    F_L = compute_flux(U_left)
    F_R = compute_flux(U_right)

    # HLL flux
    if S_L >= 0:
        return F_L
    elif S_R <= 0:
        return F_R
    else:
        return (S_R * F_L - S_L * F_R + S_L * S_R * (U_right - U_left)) / (S_R - S_L)

def apply_fvm(system):
    """
    Applies the Finite Volume Method to update the hydraulic system.
    """
    nodes = system.nodes
    delta_x = system.delta_x
    total_time = system.total_time
    CFL = system.CFL
    h_in = system.h_in
    u_in = system.u_in
    h_out = system.h_out

    num_cells = len(nodes)
    U = np.zeros((num_cells, 2))  # Conserved variables [h, hu]

    # Initialize conditions
    for i, node in nodes.items():
        h = node.flow.h
        u = node.flow.Q / node.flow.A if node.flow.A > 0 else 0.0
        U[i, 0] = h
        U[i, 1] = h * u

    t = 0.0  # Initialize time
    n = 0    # Time step counter

    while t < total_time:
        U_old = U.copy()

        # Apply boundary conditions
        U_ext = np.zeros((num_cells + 2, 2))
        U_ext[1:-1] = U

        # Upstream boundary (Inflow)
        U_ext[0, 0] = h_in
        U_ext[0, 1] = h_in * u_in

        # Downstream boundary (Specified Depth)
        U_ext[-1, 0] = h_out
        hu_out = U_ext[-2, 1]  # Assuming Neumann for momentum
        U_ext[-1, 1] = h_out * (hu_out / U_ext[-2, 0]) if U_ext[-2, 0] > 0 else 0.0

        # Compute fluxes at interfaces
        F = np.zeros((num_cells + 1, 2))
        for i in range(num_cells + 1):
            F[i] = hll_flux(U_ext[i], U_ext[i + 1])

        # Update time step based on CFL condition
        h = U[:, 0]
        hu = U[:, 1]
        u = hu / h
        c = np.sqrt(G * h)
        max_speed = np.max(np.abs(u) + c)
        dt = CFL * delta_x / max_speed if max_speed > 0 else CFL * delta_x / 1e-3
        if t + dt > total_time:
            dt = total_time - t

        # Update conserved variables
        for i in range(num_cells):
            node = nodes[i]
            S0 = node.flow.S0 if isinstance(node.flow, OpenChannel) else 0.0
            n_manning = node.flow.n if isinstance(node.flow, OpenChannel) else 0.0
            S = compute_source(U_ext[i + 1], S0, n_manning)
            U[i] = U_old[i] - (dt / delta_x) * (F[i + 1] - F[i]) + dt * S

            # Update node properties
            node.flow.h = U[i, 0]
            node.flow.Q = U[i, 1]
            node.flow.A = node.flow.b * node.flow.h if isinstance(node.flow, OpenChannel) else node.flow.A

        t += dt
        n += 1

        # Logging
        if n % 20 == 0:
            logger.info(f"Time step {n}, Time {t:.2f}s, Max Speed {max_speed:.2f} m/s")

    # Update the system's nodes with final values
    for i, node in nodes.items():
        node.flow.h = U[i, 0]
        node.flow.Q = U[i, 1]
        node.flow.A = node.flow.b * node.flow.h if isinstance(node.flow, OpenChannel) else node.flow.A
