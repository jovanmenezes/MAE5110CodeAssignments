import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

from models import rimlesswheel as model
from integrators import explicit_euler as integrator
# from integrators import rk4 as integrator

def generate_params(N):
    params = {
        "gravity": 9.81,        # gravity m/s^2
        "mass": 0.2,            # point mass at the center of the wheel (kg)
        "gamma": np.pi/10,      # slope of the ground (rad)
        "alpha": np.pi/N,       # half angle of the legs (rad)
        "radius": 0.1,          # radius of the wheel (m)
    }
    return params

def classify_state(args):
    initial_state, N = args
    params = generate_params(N)
    x = initial_state.copy()
    timestep = 1e-5
    sim_time = 5.0
    n_timesteps = int(sim_time / timestep) + 1
    time_traj = np.arange(n_timesteps) * timestep
    
    forward_impact_count = 0
    
    for step, t in enumerate(time_traj[:-1]):
        x = integrator(x_k = x, h = timestep, t = t, model = model, params = params)
        
        pos, vel = x[0], x[1]
        
        if pos >= params["gamma"] + params["alpha"] and vel > 0:
            x[0] = params["gamma"] - params["alpha"]
            x[1] = vel * np.cos(2 * params["alpha"])
            forward_impact_count += 1
            if forward_impact_count >= 10:
                return 1
        elif pos <= params["gamma"] - params["alpha"] and vel < 0:
            x[0] = params["gamma"] + params["alpha"]
            x[1] = vel * np.cos(2 * params["alpha"])
            forward_impact_count = 0
            
        if step > 10000 and abs(vel) < 1e-2:
            return 0
    return 0

def main():
    N_values = [7, 8, 9, 10, 11, 12]
    n_pts_theta = 25
    n_pts_omega = 25

    fig, axs = plt.subplots(2, 3, figsize=(18, 12))
    axs_flat = axs.flatten()

    with ProcessPoolExecutor() as executor:
        for idx, N in enumerate(N_values):
            ax = axs_flat[idx]
            params = generate_params(N)

            theta_grid = np.linspace(params["gamma"] - params["alpha"], params["gamma"] + params["alpha"], n_pts_theta)
            omega_grid = np.linspace(-4.0, 4.0, n_pts_omega)
            
            THETA, OMEGA = np.meshgrid(theta_grid, omega_grid)
            theta_pts = THETA.ravel()
            omega_pts = OMEGA.ravel()
            
            grid_points = [(np.array([t, o]), N) for t, o in zip(theta_pts, omega_pts)]
            results = list(executor.map(classify_state, grid_points))
            results = np.array(results)
            
            limit_cycle_mask = (results == 1)
            rest_mask = (results == 0)

            ax.scatter(theta_pts[rest_mask], omega_pts[rest_mask], color='blue', s=10, label='Rest State', alpha=0.7)
            ax.scatter(theta_pts[limit_cycle_mask], omega_pts[limit_cycle_mask], color='red', s=10, label='Walking Cycle', alpha=0.7)
            ax.axvline(params["gamma"] - params["alpha"], color='black', linestyle='--', label='Impact Boundaries')
            ax.axvline(params["gamma"] + params["alpha"], color='black', linestyle='--')
            
            ax.set_title(f"N = {N}", fontsize=11)
            ax.set_xlabel(r"Initial Angle $\theta_0$ (rad)", fontsize=9)
            ax.set_ylabel(r"Initial Angular Velocity $\dot{\theta}_0$ (rad/s)", fontsize=9)
            ax.legend(loc="upper left", fontsize=7)
            ax.grid(True, alpha=0.3)

    plt.suptitle("Region of Attraction Plots for Rimless Wheel Across Different Spokes ($N$)", fontsize=9)
    plt.tight_layout()
    plt.savefig("region_of_attraction_N_sweep.png", dpi=300)
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()