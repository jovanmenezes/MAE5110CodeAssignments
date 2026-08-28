def explicit_euler(x_k, h, t, params, model):
    # print("Using Euler Method")
    return x_k + h * model.dynamics(t, x_k, params)

def rk4(x_k, h, t, params, model):
    # print("Using fourth-order Runge-Kutta scheme method")
    k1 = model.dynamics(t, x_k, params)
    k2 = model.dynamics((t + h/2), (x_k + k1*h/2), params)
    k3 = model.dynamics((t + h/2), (x_k + k2*h/2), params)
    k4 = model.dynamics((t + h), (x_k + k3*h), params)
    return x_k + h*(k1 + 2*k2 + 2*k3 + k4)/6