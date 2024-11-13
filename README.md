# SynthStreamlines
A library for synthetic tractography + neuronal networks + behavioral diffeomorphisms.

## Overview

## Running Mayavi
Mayavi has issues with Wayland.
To run anything that uses Mayavi, the kludge way is to tell Qt to force-use X11

``` export QT_QPA_PLATFORM=xcb```

Before running any script.