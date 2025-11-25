#%%
%load_ext autoreload
%autoreload 2
#%%
from synth_streamlines.bundles.generator import generate_uniform_grid_streamlines
import numpy as np

n_streamlines = 100000

#%%
output_file = f"C:/Users/virat/connectomes/synthetic/rand_output_grid{n_streamlines}.trk"
grid_size = (100, 100, 100)  # Define the size of the 3D grid
generator = generate_uniform_grid_streamlines(output_file, n_streamlines, grid_size)
generator.gen_rand_streamlines(streamline_extent = 20, axes=[0,1,2])
#generator.gen_grid_streamlines(bounds=(-50,50),streamline_extent=20, axes=[0, 1, 2])#.bend_streamlines(bend_factor=5)
generator.save_streamlines_trk(save_loc=output_file)