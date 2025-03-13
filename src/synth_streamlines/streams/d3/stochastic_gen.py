# %%
import numpy as np
import matplotlib.pyplot as plt


def generate_stochastic_path(start, end, curvature, num_points=100):
    """
    Generates a stochastic path between two points with a given curvature.

    Parameters:
    start (tuple): Starting point (x, y).
    end (tuple): Ending point (x, y).
    curvature (float): Curvature factor.
    num_points (int): Number of points in the path.

    Returns:
    np.ndarray: Array of points representing the path.
    """
    x0, y0 = start
    x1, y1 = end

    # Generate linear space between start and end points
    t = np.linspace(0, 1, num_points)
    x = np.linspace(x0, x1, num_points)
    y = np.linspace(y0, y1, num_points)

    # Add stochastic curvature
    random_offsets = curvature * (np.random.rand(num_points) - 0.5)
    y += random_offsets

    return np.vstack((x, y)).T


def plot_path(path):
    """
    Plots the generated path.

    Parameters:
    path (np.ndarray): Array of points representing the path.
    """
    plt.plot(path[:, 0], path[:, 1], marker="o")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Stochastic Path with Curvature")
    plt.show()


# %%
if __name__ == "__main__":
    start_point = (0, 0)
    end_point = (10, 10)
    curvature = 1.0

    path = generate_stochastic_path(start_point, end_point, curvature)
    plot_path(path)
