import numpy as np
import matplotlib.pyplot as plt

from models import rimlesswheel as model
from integrators import explicit_euler as integrator
# from integrators import rk4 as integrator

def generate_params():
    N = 6
    params = {
        "gravity": 9.81,            # gravity m/s^2
        "mass": 0.2,                # point mass at the center of the wheel (kg)
        "gamma": np.pi/10,          # slope of the ground (rad)
        "alpha": np.pi/N,           # half angle of the legs (rad)
        "radius": 0.1,              # radius of the wheel (m)
    }
    return params

initial_state = np.array([np.pi/180*10, 2.0])
timestep = 1e-5
sim_time = 5.0
n_timesteps = int(sim_time / timestep) + 1
time_traj = np.arange(n_timesteps) * timestep
state_traj = np.zeros((initial_state.shape[0], n_timesteps))
state_traj[:, 0] = initial_state
params = generate_params()
angular_velocity = []

# simulation loop
for step, t in enumerate(time_traj[:-1]):
    state_traj[:, step + 1] = integrator(x_k = state_traj[:, step], h = timestep, t = t, model = model, params = params)
    
    if state_traj[0, step + 1] >= params["gamma"] + params["alpha"] and state_traj[1, step + 1] > 0:
        state_traj[0, step + 1] = params["gamma"] - params["alpha"]
        state_traj[1, step + 1] = state_traj[1, step + 1] * np.cos(2 * params["alpha"])
        angular_velocity.append(state_traj[1, step + 1])
    elif state_traj[0, step + 1] <= params["gamma"] - params["alpha"] and state_traj[1, step + 1] < 0:
        state_traj[0, step + 1] = params["gamma"] + params["alpha"]
        state_traj[1, step + 1] = state_traj[1, step + 1] * np.cos(2 * params["alpha"])
        angular_velocity.append(state_traj[1, step + 1])

plt.figure()
plt.plot(state_traj[0,:], state_traj[1,:], label="Phase Portrait")
plt.xlabel(r"Angle $\theta$ (rad)")
plt.ylabel(r"Angular Velocity $\dot{\theta}$ (rad/s)")
plt.title("Phase Portrait plot for the Rimless Wheel")
plt.legend()
plt.tight_layout()
plt.savefig("phase_portrait.png", dpi=300)
plt.show()
plt.close()

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
plt.savefig("energy_plot.png", dpi=300)
plt.show()
plt.close()

v_k = np.array(angular_velocity[:-1])
v_k1 = np.array(angular_velocity[1:])
all_v = np.concatenate([v_k, v_k1])
min_v, max_v = np.min(all_v) * 0.9, np.max(all_v) * 1.1
grid = np.linspace(min_v, max_v, 100)
degree = 3
coeffs = np.polyfit(v_k, v_k1, degree)
poly_func = np.poly1d(coeffs)
v_fit = np.linspace(min_v, max_v, 200)
v_fit_next = poly_func(v_fit)
identity_poly = np.poly1d([1, 0])
intersection_poly = poly_func - identity_poly
roots = intersection_poly.roots
real_roots = roots[np.isreal(roots)].real
fixed_point = [r for r in real_roots if min_v <= r <= max_v][0]
derivative_poly = np.polyder(poly_func)
slope = derivative_poly(fixed_point)
plt.figure()
plt.plot(v_k, v_k1, 'bo', label="Impact Transitions")
plt.plot(grid, grid, 'r--', label="Identity Line ($y = x$)")
plt.plot(v_fit, v_fit_next, 'g-', label="Return Map")
plt.plot(fixed_point, fixed_point, marker='*', ms=8, color='magenta', label=f"$\\dot{{\\theta}}^*$: {fixed_point:.4f} (Slope: {slope:.2f})")
plt.xlabel(r"Angular Velocity at step $k$: $\dot{\theta}_k^+$ (rad/s)")
plt.ylabel(r"Angular Velocity at step $k+1$: $\dot{\theta}_{k+1}^+$ (rad/s)")
plt.title("Poincaré Return Map for the Rimless Wheel with 6 Spokes")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.savefig("poincare_return_map.png", dpi=300)
plt.show()
plt.close()