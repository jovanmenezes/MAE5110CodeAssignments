import numpy as np
import math

def dynamics(t, state):
    params = generate_params()
    gravity = params["gravity"]
    mass = params["mass"]
    radius = params["radius"]
    Drag_Coefficient = params["Drag_Coefficient"]
    density = params["density"]
    mu = 0.5 * Drag_Coefficient * density * math.pi * radius**2 / mass
    
    vx = state[2]
    vy = state[3]
    ax = - mu * vx * math.sqrt(vx**2 + vy**2)
    ay = - gravity - mu * vy * math.sqrt(vx**2 + vy**2)

    state_derivative = np.array([vx, vy, ax, ay])
    return state_derivative

def generate_params():
    params = {
        "gravity": 9.81,  # gravity m/s^2)
        "Coefficient_of_Restitution": 0.8,  # constant that determines how much energy is dissipated upon collision
        "radius": 0.05,  # radius of the ball (m)
        "mass": 0.5, # mass of the ball (kg)
        "Drag_Coefficient": 0.47,  # drag coefficient for a sphere
        "density": 1.225,  # density of air at sea level (kg/m^3)
        }
    return params

def calculate_energy(state):
    """Compute energies for a state ``(2,)`` or trajectory ``(2, N)``."""
    params = generate_params()
    gravity = params["gravity"]
    mass = params["mass"]

    y_position = state[1]  # indexes entire row "vectorized" if state is (2, N)
    vx = state[2]
    vy = state[3]

    kinetic_energy = 0.5 * mass * (vx**2 + vy**2)
    potential_energy = mass * gravity * y_position
    return kinetic_energy, potential_energy
