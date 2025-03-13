import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class bundle:
    def __init__(self):
        pass

    def generate_streamlines(self, a, b, N, noise_level, tortuosity):
        streamlines = []
        for _ in range(N):
            t = np.linspace(0, 1, 5)  # fewer points for spline fitting
            x_points = (1 - t) * a[0] + t * b[0] + noise_level * np.random.randn(len(t))
            y_points = (1 - t) * a[1] + t * b[1] + noise_level * np.random.randn(len(t))
            z_points = (1 - t) * a[2] + t * b[2] + noise_level * np.random.randn(len(t))

            # Apply tortuosity transformation
            if tortuosity > 0:
                x_points = np.interp(
                    t, t, x_points + tortuosity * np.sin(2 * np.pi * t)
                )
                y_points = np.interp(
                    t, t, y_points + tortuosity * np.sin(2 * np.pi * t)
                )
                z_points = np.interp(
                    t, t, z_points + tortuosity * np.sin(2 * np.pi * t)
                )

            t_new = np.linspace(0, 1, 100)
            x_spline = make_interp_spline(t, x_points, k=3)(t_new)
            y_spline = make_interp_spline(t, y_points, k=3)(t_new)
            z_spline = make_interp_spline(t, z_points, k=3)(t_new)

            streamlines.append((x_spline, y_spline, z_spline))
        return streamlines

    def plot_streamlines(self, streamlines):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        for x, y, z in streamlines:
            ax.plot(x, y, z)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Generated Streamlines")
        plt.show()

    def generate_bundle(
        self,
        a=None,
        b=None,
        num_streamlines=5,
        do_plot=False,
        tortuosity=0.01,
        noise_level=0.1,
    ):
        # Example usage
        if a is None:
            a = np.array([0, 0, 0])
        if b is None:
            b = np.array([1, 1, 1])

        streamlines = self.generate_streamlines(
            a, b, num_streamlines, tortuosity=tortuosity, noise_level=noise_level
        )
        if do_plot:
            self.plot_streamlines(streamlines)

        self.streamlines = streamlines

    def plot_streamlines_with_probe(self, streamlines, x, y, z, r):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        for ss, (x_spline, y_spline, z_spline) in enumerate(streamlines):
            ax.plot(x_spline, y_spline, z_spline, label=f"s{ss}")

        # Create a sphere for the probe point
        u, v = np.linspace(0, 2 * np.pi, 100), np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        x_sphere = x + r * np.cos(u) * np.sin(v)
        y_sphere = y + r * np.sin(u) * np.sin(v)
        z_sphere = z + r * np.cos(v)

        ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color="r", linestyle="--")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.set_title("Generated Streamlines with Probe Point")
        ax.set_aspect("equal")
        plt.legend()
        plt.show()


class StreamlineChecker:
    def __init__(self):
        pass

    def check_streamlines(self, bundle, x, y, z, r):
        self._probe_point = (x, y, z, r)
        passing_streamline_indices = []
        for ss, (x_spline, y_spline, z_spline) in enumerate(bundle.streamlines):
            distances = np.sqrt(
                (x_spline - x) ** 2 + (y_spline - y) ** 2 + (z_spline - z) ** 2
            )
            if np.any(distances <= r):
                passing_streamline_indices.append(ss)
        return passing_streamline_indices
