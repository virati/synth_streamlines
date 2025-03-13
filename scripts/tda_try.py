# %%
import numpy as np

from dipy.data.fetcher import fetch_bundles_2_subjects, read_bundles_2_subjects
from dipy.tracking.streamline import Streamlines
from dipy.viz import actor, ui, window
import nibabel as nib
from ripser import ripser
from persim import plot_diagrams


def shift_streamlines(streamlines, shift_x, shift_y, shift_z):
    for streamline in streamlines:
        for point in streamline:
            point[0] += shift_x
            point[1] += shift_y
            point[2] += shift_z
    return streamlines


def mirror_streamlines(streamlines, axis, do_copy=True):
    if do_copy:
        streamlines = streamlines.copy()

    for streamline in streamlines:
        for point in streamline:
            point[axis] = -point[axis]
    return streamlines


def get_min_distances(streamlines, center_point):
    stream_min_distances = []
    for streamline in streamlines:
        stream_pointwise_distances = []
        for point in streamline:
            stream_pointwise_distances.append(np.linalg.norm(point - center_point))
        stream_min_distances.append(np.min(stream_pointwise_distances))

    return stream_min_distances


trk_file = None
use_sample_data = False
if use_sample_data:
    fetch_bundles_2_subjects()
else:
    custom_trk_path = "/home/virati/Data/postdoc/um1/linc_ome/sub-I74_sample-hemi_space-CIT168_desc-CSD_tractography.trk"
    if trk_file is None:
        trk_file = nib.streamlines.load(custom_trk_path)
        header = trk_file.header
        custom_streamlines = trk_file.streamlines

res = read_bundles_2_subjects(
    subj_id="subj_1", metrics=["t1", "fa"], bundles=["af.left", "cst.right", "cc_1"]
)
# %% Downsample and Shifts/Mirrors
N = 15  # Number of streamlines to randomly choose
random_indices = np.random.choice(len(custom_streamlines), N, replace=False)
ds_custom_streamlines = [custom_streamlines[ii] for ii in random_indices]


## integrate tda of the custom streamlines
# Function to calculate persistent homology
def calculate_persistent_homology(streamlines):
    all_points = np.concatenate(streamlines, axis=0)
    diagrams = ripser(all_points)["dgms"]
    return diagrams


# Calculate persistent homology for the downsampled streamlines
diagrams = calculate_persistent_homology(ds_custom_streamlines)

# Plot the persistence diagrams
plot_diagrams(diagrams, show=True)
# %%
electrode_position = (0.0, 0.0, 0.0)
stream_distances = get_min_distances(ds_custom_streamlines, electrode_position)
