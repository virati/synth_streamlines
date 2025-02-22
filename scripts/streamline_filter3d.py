# %%
# %load_ext autoreload
# %autoreload 2

from synth_streamlines.streams.d3 import generate as gen
import matplotlib.pyplot as plt

probe_point = {"x": 0.5, "y": 0.5, "z": 0.5, "r": 2}
test = gen.bundle()
test.generate_bundle(do_plot=False, tortuosity=0.01, noise_level=10)
test.plot_streamlines_with_probe(test.streamlines, **probe_point)
# %%
ff_task = gen.StreamlineChecker()
print(ff_task.check_streamlines(test, **probe_point))
