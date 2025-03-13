# %%
# %load_ext autoreload
# %autoreload 2

from synth_streamlines.streams.d3 import generate as gen
import matplotlib.pyplot as plt

test = gen.bundle()
test.generate_bundle(
    a=(-10, -10, -10),
    b=(10, -10, 10),
    do_plot=False,
    tortuosity=0.01,
    noise_level=10.0,
    num_streamlines=20,
)
# %%
probe_point = {"x": 0.0, "y": 0.0, "z": 0.0, "r": 6}
test.plot_streamlines_with_probe(test.streamlines, **probe_point)
ff_task = gen.StreamlineChecker()
print(ff_task.check_streamlines(test, **probe_point))
print("Done")
