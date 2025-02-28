import numpy as np

from dipy.data.fetcher import fetch_bundles_2_subjects, read_bundles_2_subjects
from dipy.tracking.streamline import Streamlines
from dipy.viz import actor, ui, window

fetch_bundles_2_subjects()

res = read_bundles_2_subjects(
    subj_id="subj_1", metrics=["t1", "fa"], bundles=["af.left", "cst.right", "cc_1"]
)

streamlines = Streamlines(res["af.left"])
streamlines.extend(res["cst.right"])
streamlines.extend(res["cc_1"])

data = res["fa"]
shape = data.shape
affine = res["affine"]
