import numpy as np
import matplotlib.pyplot as plt

from models import rimlesswheel as model
from integrators import explicit_euler as integrator
# from integrators import rk4 as integrator

initial_state = np.array([np.pi/180*30 + 0.9*np.pi/180*(180/6), -4.0])

timestep = 1e-5
sim_time = 5.0

n_timesteps = int(sim_time / timestep) + 1
time_traj = np.arange(n_timesteps) * timestep
state_traj = np.zeros((initial_state.shape[0], n_timesteps))
state_traj[:, 0] = initial_state
params = model.generate_params()

angular_velocity = []

# simulation loop
for step, t in enumerate(time_traj[:-1]):
    state_traj[:, step + 1] = integrator(x_k = state_traj[:, step], h = timestep, t = t, model = model)
    
    if state_traj[0, step + 1] >= params["gamma"] + params["alpha"] and state_traj[1, step + 1] > 0:
        # angular_velocity.append(state_traj[1, step + 1])
        state_traj[0, step + 1] = params["gamma"] - params["alpha"]
        state_traj[1, step + 1] = state_traj[1, step + 1] * np.cos(2 * params["alpha"])
        angular_velocity.append(state_traj[1, step + 1])
    elif state_traj[0, step + 1] <= params["gamma"] - params["alpha"] and state_traj[1, step + 1] < 0:
        # angular_velocity.append(state_traj[1, step + 1])
        state_traj[0, step + 1] = params["gamma"] + params["alpha"]
        state_traj[1, step + 1] = state_traj[1, step + 1] * np.cos(2 * params["alpha"])
        angular_velocity.append(state_traj[1, step + 1])

v_k = np.array(angular_velocity[:-1])
v_k1 = np.array(angular_velocity[1:])

plt.figure()
plt.plot(v_k, v_k1, 'bo', label="Impact Transitions")
all_v = np.concatenate([v_k, v_k1])
min_v, max_v = np.min(all_v) * 0.9, np.max(all_v) * 1.1
grid = np.linspace(min_v, max_v, 100)
plt.plot(grid, grid, 'r--', label="Identity Line ($y = x$)")
plt.xlabel(r"Angular Velocity at step $k$: $\dot{\theta}_k^-$ (rad/s)")
plt.ylabel(r"Angular Velocity at step $k+1$: $\dot{\theta}_{k+1}^-$ (rad/s)")
plt.title("Poincaré Return Map for Rimless Wheel")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.show()

kinetic_energy, potential_energy = model.calculate_energy(state_traj)
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

plt.figure()
plt.plot(state_traj[0,:], state_traj[1,:], label="Phase Portrait")
plt.xlabel("Angle (rad)")
plt.ylabel("Angular Velocity (rad/s)")
plt.title("Phase Portrait Plot for a Rimless Wheel")
plt.legend()
plt.tight_layout()
plt.show()