import numpy as np

def dynamics(t, state):
    params = generate_params()
    gravity = params["gravity"]
    cor = params["Coefficient_of_Restitution"]

    position = state[0]
    velocity = state[1]
    acceleration = - gravity

    state_derivative = np.array([velocity, acceleration])
    return state_derivative

def generate_params():
    params = {
        "gravity": 9.81,  # gravity m/s^2)
        "Coefficient_of_Restitution": 0.8,  # constant that determines how much energy is dissipated upon collision
        "radius": 0.05,  # radius of the ball (m)
        "mass": 0.05 # mass of the ball (kg)
        }
    return params

def calculate_energy(state):
    """Compute energies for a state ``(2,)`` or trajectory ``(2, N)``."""
    params = generate_params()
    gravity = params["gravity"]
    mass = params["mass"]

    position = state[0]  # indexes entire row "vectorized" if state is (2, N)
    velocity = state[1]

    kinetic_energy = 0.5 * mass * (velocity) ** 2
    potential_energy = mass * gravity * position
    return kinetic_energy, potential_energy
