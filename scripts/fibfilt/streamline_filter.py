# %%
%load_ext autoreload
%autoreload 2

from synth_streamlines.streams.d2 import generate as gen
import matplotlib.pyplot as plt

probe_point = (0.5, 0.5,0.1)
test = gen.bundle()
test.generate_bundle(do_plot=True, tortuosity=0.0001, noise_level=0.1)
test.plot_streamlines_with_probe(test.streamlines, *probe_point)
# %%
ff_task = gen.StreamlineChecker()
ff_task.check_streamlines(test, *probe_point)