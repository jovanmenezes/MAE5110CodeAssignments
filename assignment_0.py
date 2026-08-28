import numpy as np
import matplotlib.pyplot as plt

# from models import pendulum as model
from models import bouncingball as model
from integrators import explicit_euler as integrator
# from integrators import rk4 as integrator

# Basic simulation of the pendulum

# params = {
#     "gravity": 9.81,  # gravity m/s^2)
#     "length": 1,  # rod length (m)
#     "mass": 0.2,  # point mass at end of rod (kg)
#     "damping_coeff": 0.0,  # damping coefficient (kg*m^2/s)
# }

params = {
        "gravity": 9.81,  # gravity m/s^2)
        "Coefficient_of_Restitution": 0.8,  # constant that determines how much energy is dissipated upon collision
        "radius": 0.05,  # radius of the ball (m)
        "mass": 0.05 # mass of the ball (kg)
        }

# some set-up
# initial_state = np.array([np.pi / 4, 0.0])
initial_state = np.array([10 , 0.0])

timestep = 1e-5
sim_time = 5.0

n_timesteps = int(sim_time / timestep) + 1
time_traj = np.arange(n_timesteps) * timestep
state_traj = np.zeros((2, n_timesteps))
state_traj[:, 0] = initial_state

# simulation loop
for step, t in enumerate(time_traj[:-1]):
    # state_traj[:, step + 1] = state_traj[:, step] + timestep * model.dynamics(
    #     t, state_traj[:, step], params
    # )
    state_traj[:, step + 1] = integrator(x_k = state_traj[:, step], h = timestep, t = t, params = params, model = model)
    if state_traj[0, step + 1] < params["radius"]:
        state_traj[0, step + 1] = params["radius"]
        state_traj[1, step + 1] = - params["Coefficient_of_Restitution"] * state_traj[1, step]

# sanity check the energies: since there is no actuation, and no damping, total energy should stay
# constant. If we turn on the damping coefficient, it should slowly bleed out energy until it comes to
# a stand-still.

kinetic_energy, potential_energy = model.calculate_energy(state_traj, params)

plt.figure()
plt.plot(time_traj, potential_energy, label="Potential energy")
plt.plot(time_traj, kinetic_energy, label="Kinetic energy")
plt.plot(time_traj, potential_energy + kinetic_energy, label="Total energy")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.title("Energy plot")
plt.legend()
plt.tight_layout()
plt.show()

# TODO: make a phase portrait plot
# plt.figure()
# plt.plot(state_traj[0,:], state_traj[1,:], label="Phase Portrait")
# plt.xlabel("Angle (rad)")
# plt.ylabel("Angular Velocity (rad/s)")
# plt.title("Phase Portrait Plot for a Simple Pendulum")
# plt.legend()
# plt.axis('equal')
# plt.tight_layout()
# plt.show()

plt.figure()
plt.plot(time_traj, state_traj[0,:], label="Position")
plt.ylabel("Vertical Position (m)")
plt.xlabel("Time (s)")
plt.title("Position vs. Time for a bouncing ball")
plt.legend()
plt.tight_layout()
plt.show()