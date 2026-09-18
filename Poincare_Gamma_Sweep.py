import numpy as np
import matplotlib.pyplot as plt

from models import rimlesswheel as model
from integrators import explicit_euler as integrator
# from integrators import rk4 as integrator

def generate_params(gamma, N=6):
    params = {
        "gravity": 9.81,            # gravity m/s^2
        "mass": 0.2,                # point mass at the center of the wheel (kg)
        "gamma": gamma,             # slope of the ground (rad)
        "alpha": np.pi/N,           # half angle of the legs (rad)
        "radius": 0.1,              # radius of the wheel (m)
    }
    return params

gamma_values = np.linspace(np.pi/10, np.pi/4, 13)[1:]
initial_state = np.array([np.pi/180*10, 2.0])
timestep = 1e-5
sim_time = 5.0

fig, axs = plt.subplots(3, 4, figsize=(18, 12))
axs_flat = axs.flatten()

for idx, gamma in enumerate(gamma_values):
    ax = axs_flat[idx]
    params = generate_params(gamma)
    
    n_timesteps = int(sim_time / timestep) + 1
    time_traj = np.arange(n_timesteps) * timestep
    state_traj = np.zeros((initial_state.shape[0], n_timesteps))
    state_traj[:, 0] = initial_state

    angular_velocity = []

    # Simulation loop
    for step, t in enumerate(time_traj[:-1]):
        state_traj[:, step + 1] = integrator(x_k=state_traj[:, step], h=timestep, t=t, model=model, params=params)
        
        if state_traj[0, step + 1] >= params["gamma"] + params["alpha"] and state_traj[1, step + 1] > 0:
            state_traj[0, step + 1] = params["gamma"] - params["alpha"]
            state_traj[1, step + 1] = state_traj[1, step + 1] * np.cos(2 * params["alpha"])
            angular_velocity.append(state_traj[1, step + 1])
        elif state_traj[0, step + 1] <= params["gamma"] - params["alpha"] and state_traj[1, step + 1] < 0:
            state_traj[0, step + 1] = params["gamma"] + params["alpha"]
            state_traj[1, step + 1] = state_traj[1, step + 1] * np.cos(2 * params["alpha"])
            angular_velocity.append(state_traj[1, step + 1])

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
    ax.plot(v_k, v_k1, 'bo', ms=2, label="Impacts")
    ax.plot(grid, grid, 'r--', label="Identity")
    ax.plot(v_fit, v_fit_next, 'g-', label="Return Map")
    ax.plot(fixed_point, fixed_point, marker='*', ms=6, color='magenta', label=f"FP: {fixed_point:.2f} (s: {slope:.2f})")
    gamma_deg = np.degrees(gamma)
    ax.set_title(f"$\\gamma$ = {gamma_deg:.1f}°", fontsize=8)
    ax.set_xlabel(r"$\dot{\theta}_k^+$", fontsize=8)
    ax.set_ylabel(r"$\dot{\theta}_{k+1}^+$", fontsize=8)
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    ax.legend(fontsize=6, loc="upper left")

plt.suptitle("Poincaré Return Maps for Rimless Wheel Across Different Slopes ($\gamma$)", fontsize=8)
plt.tight_layout()
plt.savefig("Poincare_Gamma_Sweep.png", dpi=300)
plt.show()
plt.close()