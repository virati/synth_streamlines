#%%
%load_ext autoreload
%autoreload 2
#%%
import numpy as np
import nibabel as nib
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.streamline import save_tractogram
from dipy.data.fetcher import fetch_mni_template

class generate_uniform_grid_streamlines:
    
    """
    Generate a .trk file with N streamlines uniformly distributed in a 3D grid.

    Parameters:
        output_file (str): Path to save the .trk file.
        n_streamlines (int): Number of streamlines to generate.
        grid_size (tuple): Size of the 3D grid (x, y, z).
    """
    def __init__(self,output_file, n_streamlines, grid_size):
    # Generate grid points
        x = np.linspace(0, grid_size[0], int(np.cbrt(n_streamlines)))
        y = np.linspace(0, grid_size[1], int(np.cbrt(n_streamlines)))
        z = np.linspace(0, grid_size[2], int(np.cbrt(n_streamlines)))
        self.grid_points = np.array(np.meshgrid(x, y, z)).T.reshape(-1, 3)

        self.mni_reference = fetch_mni_template()

    def gen_streamlines(self):
        # Create streamlines as straight lines
        streamlines = []
        grid_points = self.grid_points
        for point in grid_points:
            streamline = np.array([point, point + np.random.uniform(-1, 1, size=3)])
            streamlines.append(streamline)

        self.streamlines = streamlines

    def save_streamlines_trk(self):
        streamlines = self.streamlines 
        # Create Tractogram
        tractogram = StatefulTractogram(streamlines, reference=self.mni_reference, space=Space.VOX)

        # Create and save .trk file
        save_tractogram(tractogram, "rpt_1000.trk")
        print(f"Saved {n_streamlines} streamlines to {output_file}")

#%%

output_file = "/tmp/grid_output.trk"
n_streamlines = 1000
grid_size = (100, 100, 100)  # Define the size of the 3D grid
generator = generate_uniform_grid_streamlines(output_file, n_streamlines, grid_size)
generator.gen_streamlines()
generator.save_streamlines_trk()