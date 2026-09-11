# Assignment 1

`uv run assignment_1.py`

`uv run RoA.py`

`uv run Poincare_Gamma_Sweep.py`

`uv run Poincare_N_Sweep.py`

`uv run RoA_Gamma_Sweep.py`

`uv run RoA_N_Sweep.py`

## Model: the Rimless Wheel
1. An explanation of your sanity checks, including what you expected and what happened. **(5 pts)**

    The first sanity check used to verify the correctness of the model was the energy conservation test. For a positive incline angle, $\gamma > 0$, an initial angular position satisfying $(\gamma - \alpha) < \theta < (\gamma + \alpha)$, and a small initial angular velocity, $\dot{\theta} = 1$, the rimless wheel should roll down the incline. The system's total mechanical energy should remain approximately constant between impacts, while energy is redistributed between kinetic and potential forms At each foot-ground impact, the wheel experiences a sudden reduction in kinetic energy due to the inelastic collision, accompanied by a corresponding increase in potential energy as the wheel transitions to the next support leg. After the system converges to its stable limit cycle, the total energy should exhibit a consistent periodic behavior rather than an unbounded increase or decrease. This behavior is observed in the energy plot below, indicating that the model's energy dynamics are consistent with the expected behavior of the rimless wheel.

    ![alt text](figures\energy_plot.png)

    The second sanity check was the phase portrait. For a rimless wheel rolling down an incline, the phase portrait should converge to a stable limit cycle. This limit cycle represents the steady, periodic rolling motion of the system, in which continuous pendulum-like motion between impacts is followed by discrete changes in angular velocity when the next leg strikes the ground. As shown in the phase portrait below, the trajectory converges toward a closed, repeating orbit, demonstrating that the model exhibits the expected stable periodic rolling behavior.

    ![alt text](figures\phase_portrait.png)

## Analysis
1. A state-space plot showing the RoA of every stable attractor, including fixed points and limit cycles. **(5 pts)**

    ![alt text](figures\region_of_attraction.png)

2. One-dimensional return-map plot, with its fixed point and the identity line clearly marked. **(5 pts)**
    
    ![alt text](figures\poincare_return_map.png)

3. Visualization and discussion of how the slope and number of spokes affects the RoA and local convergence **(10 pts)**

    ![alt text](figures\poincare_N_sweep.png)
    ![alt text](figures\Poincare_Gamma_Sweep.png)
    ![alt text](figures\region_of_attraction_N_sweep.png)
    ![alt text](figures\region_of_attraction_gamma_sweep.png)


