import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

from models import rimlesswheel as model
from integrators import explicit_euler as integrator
# from integrators import rk4 as integrator

params = model.generate_params()

def classify_state(initial_state):
    x = initial_state.copy()
    timestep = 1e-5
    sim_time = 5.0
    n_timesteps = int(sim_time / timestep) + 1
    time_traj = np.arange(n_timesteps) * timestep
    
    forward_impact_count = 0
    
    for step, t in enumerate(time_traj[:-1]):
        x = integrator(x_k = x, h = timestep, t = t, model = model)
        
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
    n_pts_theta = 20
    n_pts_omega = 20

    theta_grid = np.linspace(params["gamma"] - params["alpha"], params["gamma"] + params["alpha"], n_pts_theta)
    omega_grid = np.linspace(-4.0, 4.0, n_pts_omega)
    
    THETA, OMEGA = np.meshgrid(theta_grid, omega_grid)
    
    theta_pts = THETA.ravel()
    omega_pts = OMEGA.ravel()
    grid_points = [np.array([t, o]) for t, o in zip(theta_pts, omega_pts)]
    
    print(f"Simulating {len(grid_points)} grid points in parallel...")
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(classify_state, grid_points))
        
    results = np.array(results)
    
    limit_cycle_mask = (results == 1)
    rest_mask = (results == 0)

    plt.figure()
    plt.scatter(theta_pts[rest_mask], omega_pts[rest_mask], color='blue', s=15, label='Rest State (0)', alpha=0.7)
    plt.scatter(theta_pts[limit_cycle_mask], omega_pts[limit_cycle_mask], color='red', s=15, label='Limit Cycle (1)', alpha=0.7)
    plt.axvline(params["gamma"] - params["alpha"], color='black', linestyle='--', label='Impact Boundaries')
    plt.axvline(params["gamma"] + params["alpha"], color='black', linestyle='--')
    plt.axvline(params["gamma"], color='green', linestyle=':', label=r'Rest Equilibrium ($\theta = \gamma$)')
    plt.xlabel(r"Initial Angle $\theta_0$ (rad)")
    plt.ylabel(r"Initial Angular Velocity $\dot{\theta}_0$ (rad/s)")
    plt.title("Region of Attraction Scatter Plot for the Rimless Wheel")
    plt.legend(loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    plt.savefig("region_of_attraction.png", dpi=300)

if __name__ == "__main__":
    main()
