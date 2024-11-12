import networkx as nx
import pyvista as pv
import numpy as np


# Create a NetworkX graph
G = nx.karate_club_graph()

# Extract node positions
pos = nx.spring_layout(G, seed=42)

# Create PyVista points from node positions
points = pv.PolyData()
points.points = np.array([pos[v] for v in G.nodes])

# Create PyVista lines from edges
lines = []
for u, v in G.edges:
    line = pv.Line(pos[u], pos[v])
    lines.append(line)

# Plot the network
plotter = pv.Plotter()
plotter.add_mesh(points, color='blue', render_points_as_spheres=True)
for line in lines:
    plotter.add_mesh(line, color='black')
plotter.show()