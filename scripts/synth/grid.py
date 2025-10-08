#%%
%load_ext autoreload
%autoreload 2
#%%
import numpy as np
import nibabel as nib
import nilearn
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.streamline import save_tractogram
from nilearn.datasets import load_mni152_template

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
        x = np.linspace(-grid_size[0], grid_size[0], int(np.cbrt(n_streamlines)))
        y = np.linspace(-grid_size[1], grid_size[1], int(np.cbrt(n_streamlines)))
        z = np.linspace(-grid_size[2], grid_size[2], int(np.cbrt(n_streamlines)))
        self.grid_points = np.array(np.meshgrid(x, y, z)).T.reshape(-1, 3)

        self.mni_reference = load_mni152_template()

    def gen_det_grid_lines(self,bounds=(-100, 100), density=10, line_length=200):
        """
        Generate a list of 3D line start and end points forming a grid.

        Parameters:
            bounds (tuple): (min, max) bounds in each dimension.
            density (int): Number of grid lines per axis.
            line_length (float): Length of each line (assumed to stretch from one boundary to the other).

        Returns:
            lines (list): List of (start, end) tuples, each a pair of (x, y, z).
        """
        grid_vals = np.linspace(bounds[0], bounds[1], density)
        min_b, max_b = bounds

        lines = []
        # X-direction lines
        for y in grid_vals:
            for z in grid_vals:
                start = (min_b, y, z)
                end   = (max_b, y, z)
                lines.append((start, end))
        # Y-direction lines
        for x in grid_vals:
            for z in grid_vals:
                start = (x, min_b, z)
                end   = (x, max_b, z)
                lines.append((start, end))
        # Z-direction lines
        for x in grid_vals:
            for y in grid_vals:
                start = (x, y, min_b)
                end   = (x, y, max_b)
                lines.append((start, end))

        self.streamlines = self.apply_affine(lines)
        return self
    
    def apply_affine(self, points):
        affine = np.linalg.inv(self.mni_reference.affine)
        transformed_points = np.dot(np.array(points), (affine[:3,:3]).T) + affine[:3,3]
        return transformed_points
    
    def gen_det_streamlines(self, streamline_extent = 10, axes=[0,1,2]):
        # Create streamlines as straight lines
        streamlines = []
        grid_points = self.grid_points
        for axis in axes:
            det_stream = np.array([0,0,0])
            det_stream[axis] = 1
            for point in grid_points:
                streamline = np.array([point, point + det_stream * streamline_extent])
                streamlines.append(streamline)

        #apply affine to match reference
        self.streamlines = self.apply_affine(streamlines)

        return self
    def gen_rand_streamlines(self, streamline_extent = 100):
        # Create streamlines as straight lines
        streamlines = []
        grid_points = self.grid_points
        for point in grid_points:
            streamline = np.array([point, point + np.random.uniform(-streamline_extent, streamline_extent, size=3)])
            streamlines.append(streamline)

        #apply affine to match reference
        self.streamlines = self.apply_affine(streamlines)

        return self

    
    def bend_streamlines(self, bend_factor = 0.1):
        bent_streamlines = []
        for i, sl in enumerate(self.streamlines):
            #need to switch to alleotary? so we can get a true "bend" with endpoints fixed
            noise = np.random.normal(scale=bend_factor * (i / len(self.streamlines)), size=sl.shape)
            bent_sl = sl + noise
            bent_streamlines.append(bent_sl)
        self.streamlines = bent_streamlines

        return self

    def save_streamlines_trk(self, save_loc = None):
        streamlines = self.streamlines 
        # Create Tractogram
        tractogram = StatefulTractogram(streamlines, reference=self.mni_reference, space=Space.VOX)
        tractogram.remove_invalid_streamlines()
        # Create and save .trk file
        save_tractogram(tractogram, save_loc)
        print(f"Saved {len(streamlines)} streamlines to {save_loc}")

        return self

#%%

#output_file = "/tmp/grid_output.trk"

n_streamlines = 50000
output_file = f"C:/Users/virat/connectomes/synthetic/grid_output_det{n_streamlines}.trk"
grid_size = (100, 100, 100)  # Define the size of the 3D grid
generator = generate_uniform_grid_streamlines(output_file, n_streamlines, grid_size)
generator.gen_det_streamlines(streamline_extent=10, axes=[0, 1, 2])#.bend_streamlines(bend_factor=5)
generator.save_streamlines_trk(save_loc=output_file)