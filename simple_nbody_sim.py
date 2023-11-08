import numpy as np

G = -6.67408 * 10**-11


def a_grav2(objects):
    """
    Just like a_grav, but with half the computation (roughly), because it makes
    use of Fij = -Fji
    Note: Cannot handle additional arguments like a_gra
    """
    Fx_mat = np.zeros((len(objects[0]), len(objects[0])))
    Fy_mat = np.zeros((len(objects[0]), len(objects[0])))
    for i in range(len(objects[0])):
        x1, y1, vx1, vy1, m1 = objects[:, i]
        for j in range(i + 1, len(objects[0])):
            x2, y2, vx2, vy2, m2 = objects[:, j]
            r = dist(x1, x2, y1, y2)
            angle = np.arctan((y1 - y2) / (x1 - x2))
            F = G * m1 * m2 / r**2
            Fx = F * np.cos(angle)
            Fy = F * np.sin(angle)
            if x1 > x2:
                Fx_mat[i][j] += Fx
                Fy_mat[i][j] += Fy
                Fx_mat[j][i] -= Fx
                Fy_mat[j][i] -= Fy
            else:
                Fx_mat[i][j] -= Fx
                Fy_mat[i][j] -= Fy
                Fx_mat[j][i] += Fx
                Fy_mat[j][i] += Fy
    ax_array = np.array([np.sum(Fx) for Fx in Fx_mat]) / objects[-1]
    ay_array = np.array([np.sum(Fy) for Fy in Fy_mat]) / objects[-1]
    return np.array([ax_array, ay_array])


def a_grav(objects):
    """
    A very basic gravitational acceleration calculator
    :param objects:
    :return:
    """
    x_dists = objects[0] - objects[0].reshape(-1, 1)
    y_dists = objects[1] - objects[1].reshape(-1, 1)
    r_squar = x_dists**2 + y_dists**2
    G_grav = G * objects[4] * objects[4].reshape(-1, 1) / r_squar**1.5
    Fx = x_dists * G_grav
    Fy = y_dists * G_grav
    np.fill_diagonal(Fx, 0)
    np.fill_diagonal(Fy, 0)
    ax = np.sum(Fx, axis=0) / objects[4]
    ay = np.sum(Fy, axis=0) / objects[4]
    return np.array([ax, ay])


def rk4(x, dt):
    """
    Applies a fourth order runge-kutta numerical integration method to a
    variable x with differtation function (?) "function" with a time step of dt
    Returns the new value for "x"
    """
    k1 = step_function(x)
    k2 = step_function(x + k1 * dt * 0.5)
    k3 = step_function(x + k2 * dt * 0.5)
    k4 = step_function(x + k3 * dt)
    x += (k1 + 2 * k2 + 2 * k3 + k4) * (dt / 6.)
    return x


def step_function(objects):
    """
    Returns the derivatives of the position and velocity of the objects
    Note, *args is only there to be compatible with the general form of RK4.
    """
    d_objects = np.zeros(np.shape(objects))
    d_objects[0] = objects[2]
    d_objects[1] = objects[3]
    a_array = a_grav(objects)
    d_objects[2] = a_array[0]
    d_objects[3] = a_array[1]
    return d_objects


def dist(x1, x2, y1, y2):
    """
    Calculates the hypotenuse side of a triangle defined by x1, x2, y1, y2
    """
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
