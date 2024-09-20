import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
G = 9.81  # Gravitational acceleration (m/s^2)

# Simulation parameters
num_cells = 100
L = 1000.0  # Length of the channel (m)
dx = L / num_cells
CFL = 0.9  # CFL number
total_time = 200.0  # Total simulation time (s)

# Channel parameters
S0 = 0.001  # Bed slope
n = 0.03  # Manning's roughness coefficient
b = 5.0  # Channel width (m)

# Initial conditions
def initial_conditions(x):
    h0 = 2.0  # Initial depth (m)
    u0 = 0.0  # Initial velocity (m/s)
    return h0, u0

# Boundary conditions
def boundary_conditions(U_left, U_right, t):
    # Upstream boundary (inflow)
    h_in = 2.0  # Upstream depth (m)
    u_in = 2.0  # Upstream velocity (m/s)
    U_left[0] = h_in
    U_left[1] = h_in * u_in

    # Downstream boundary (outflow)
    U_right[0] = U_right[0]  # Neumann boundary condition (zero gradient)
    U_right[1] = U_right[1]

# Compute fluxes
def compute_flux(U):
    h = U[0]
    hu = U[1]
    u = hu / h
    flux = np.array([hu, hu * u + 0.5 * G * h * h])
    return flux

# Compute source term
def compute_source(U):
    h = U[0]
    hu = U[1]
    u = hu / h
    Sf = G * n * n * u * abs(u) / (h ** (4 / 3))
    S = np.array([0.0, -G * h * S0 - G * h * Sf])
    return S

# HLL Riemann solver
def hll_flux(U_left, U_right):
    # Left state
    h_L = U_left[0]
    hu_L = U_left[1]
    u_L = hu_L / h_L
    c_L = np.sqrt(G * h_L)

    # Right state
    h_R = U_right[0]
    hu_R = U_right[1]
    u_R = hu_R / h_R
    c_R = np.sqrt(G * h_R)

    # Compute wave speeds
    S_L = min(u_L - c_L, u_R - c_R)
    S_R = max(u_L + c_L, u_R + c_R)

    # Compute fluxes
    F_L = compute_flux(U_left)
    F_R = compute_flux(U_right)

    if S_L >= 0:
        return F_L
    elif S_L <= 0 <= S_R:
        return (S_R * F_L - S_L * F_R + S_L * S_R * (U_right - U_left)) / (S_R - S_L)
    else:  # S_R <= 0
        return F_R

# Main simulation function
def run_simulation():
    dt = 0.5  # Initialize dt
    # Spatial grid
    x = np.linspace(0, L, num_cells)
    U = np.zeros((num_cells, 2))  # Conserved variables [h, hu]

    # Initialize conditions
    for i in range(num_cells):
        h0, u0 = initial_conditions(x[i])
        U[i, 0] = h0
        U[i, 1] = h0 * u0

    # Time integration
    t = 0.0  # Initialize time
    n = 0    # Time step counter
    while t < total_time:
        U_old = U.copy()

        # Apply boundary conditions
        U_ext = np.zeros((num_cells + 2, 2))
        U_ext[1:-1] = U
        boundary_conditions(U_ext[0], U_ext[-1], t)

        # Compute fluxes at interfaces
        F = np.zeros((num_cells + 1, 2))
        for i in range(num_cells + 1):
            F[i] = hll_flux(U_ext[i], U_ext[i + 1])

        # Update conserved variables
        for i in range(num_cells):
            S = compute_source(U_ext[i + 1])
            U[i] = U_old[i] - (dt / dx) * (F[i + 1] - F[i]) + dt * S

        # Update time step based on CFL condition
        h = U[:, 0]
        hu = U[:, 1]
        u = hu / h
        c = np.sqrt(G * h)
        max_speed = np.max(abs(u) + c)
        dt = CFL * dx / max_speed
        if t + dt > total_time:
            dt = total_time - t

        t += dt
        n += 1

        # Logging
        if n % 20 == 0:
            logger.info(f"Time step {n}, Time {t:.2f}s, Max Speed {max_speed:.2f} m/s")

    return x, U

# Plot results
def plot_results(x, U):
    h = U[:, 0]
    hu = U[:, 1]
    u = hu / h

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(x, h, label='Water Depth h (m)')
    plt.xlabel('Distance (m)')
    plt.ylabel('Depth (m)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(x, u, label='Velocity u (m/s)')
    plt.xlabel('Distance (m)')
    plt.ylabel('Velocity (m/s)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    x, U = run_simulation()
    plot_results(x, U)
