import numpy as np


def dynamics(t, state):
    params = generate_params()
    gravity = params["gravity"]
    radius = params["radius"]
    mass = params["mass"]

    angle = state[0]
    angular_velocity = state[1]

    angular_acceleration = (
        mass * gravity * radius * np.sin(angle)
    ) / (mass * radius**2)

    state_derivative = np.array([angular_velocity, angular_acceleration])
    return state_derivative


def generate_params():
    params = {
        "gravity": 9.81,  # gravity m/s^2)
        "mass": 0.2,  # point mass at the center of the wheel (kg)
        "gamma": np.pi/180*30,  # slope of the ground (rad)
        "alpha": np.pi/180*(180/6),  # half angle of the legs (rad)
        "radius": 0.1,  # radius of the wheel (m)
    }
    return params


def calculate_energy(state):
    """Compute energies for a state ``(2,)`` or trajectory ``(2, N)``."""
    params = generate_params()
    gravity = params["gravity"]
    radius = params["radius"]
    mass = params["mass"]

    angle = state[0]  # indexes entire row "vectorized" if state is (2, N)
    angular_velocity = state[1]

    kinetic_energy = 0.5 * mass * (radius * angular_velocity) ** 2
    potential_energy = mass * gravity * radius * np.cos(angle)
    return kinetic_energy, potential_energy
