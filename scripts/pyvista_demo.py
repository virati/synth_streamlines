from __future__ import annotations

import time

import pyvista as pv
from pyvista import examples

lidar = examples.download_lidar()

tstart = time.time()
clipped = lidar.clip(origin=(0, 0, 1.76e3), normal=(0, 0, 1))
t_elapsed = time.time() - tstart
print(f"Time to clip with a PolyData {t_elapsed:.2f} seconds.")