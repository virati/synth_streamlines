#%%
import numpy as np
from aleatory.processes import BrownianBridge
import matplotlib.pyplot as plt


#%%
def brownbridge_process(T,N,num_paths=1, base_curve = False):
    process = BrownianBridge(initial=-2,end=2)
    paths = process.simulate(n=N, N=num_paths)
    if base_curve:
        tvec = np.linspace(0,1, N)
        
        paths = [path + 2*np.sin(2 * np.pi * 1 * tvec) for path in paths]
    return paths

# Generate some data for the line plot
x = brownbridge_process(1,300)
y = brownbridge_process(1,300)
z = brownbridge_process(1,300)



# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the line
ax.plot(x, y, z)
ax.set_xlim(-3,3)
ax.set_ylim(-3,3)
ax.set_zlim(-3,3)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Line Plot')

# Show the plot
plt.show()