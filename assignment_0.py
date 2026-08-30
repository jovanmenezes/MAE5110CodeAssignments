import timeit
import numpy as np
import matplotlib.pyplot as plt

# from models import pendulum as model
from models import bouncingball as model
from integrators import explicit_euler as integrator
# from integrators import rk4 as integrator

# Basic simulation of the pendulum

# some set-up
# initial_state = np.array([np.pi / 4, 0.0])
initial_state = np.array([0, 10, -3, 4.0])

timestep = 1e-5                 # max_timestep = 0.000709 (Euler)       max_timestep = 0.22049 (RK4)
sim_time = 5.0

n_timesteps = int(sim_time / timestep) + 1
time_traj = np.arange(n_timesteps) * timestep
state_traj = np.zeros((initial_state.shape[0], n_timesteps))
state_traj[:, 0] = initial_state

# simulation loop
for step, t in enumerate(time_traj[:-1]):
    # state_traj[:, step + 1] = state_traj[:, step] + timestep * model.dynamics(
    #     t, state_traj[:, step], params
    # )
    
    state_traj[:, step + 1] = integrator(x_k = state_traj[:, step], h = timestep, t = t, model = model)
    
    params = model.generate_params()
    if state_traj[1, step + 1] < params["radius"]:
        state_traj[1, step + 1] = params["radius"]
        state_traj[3, step + 1] = - params["Coefficient_of_Restitution"] * state_traj[3, step]
                
    # print(min(timeit.repeat(
    #             lambda: integrator(x_k = state_traj[:, step], h = timestep, t = t, model = model),
    #             repeat=1, number = 1
    #         )))
    # timeit ~ 1.5e-5 (Euler)                   timeit ~ 4.5e-5 (RK4)
    # timeit ~ 1.3e-5 (Euler max_timestep)      timeit ~ 4.0e-5 (RK4 max_timestep)
        

# sanity check the energies: since there is no actuation, and no damping, total energy should stay
# constant. If we turn on the damping coefficient, it should slowly bleed out energy until it comes to
# a stand-still.

kinetic_energy, potential_energy = model.calculate_energy(state_traj)

# initial_energy = kinetic_energy[0] + potential_energy[0]
# final_energy = kinetic_energy[-1] + potential_energy[-1]
# energy_change = (final_energy - initial_energy)/initial_energy
# if abs(energy_change) > 0.03:
#         print("Discretization step is too large!!!")

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
plt.plot(state_traj[0,:], state_traj[1,:], label="Position")
plt.ylabel("Vertical Position (m)")
plt.xlabel("Horizontal Position (m)")
plt.title("x-y Position for a bouncing ball")
plt.legend()
plt.tight_layout()
plt.show()