import numpy as np
from dipy.io.streamline import load_tractogram
from dipy.tracking.streamline import Streamlines
from dipy.viz import actor, ui, window


class StreamlineVisualizer:
    def __init__(self, trk_file=None):
        if trk_file is None:
            raise ValueError("Please provide a path to a .trk file")
        self.trk_file = trk_file

        self.streamlines = None
        self.data = None
        self.affine = None
        self.shape = None
        self.scene = window.Scene()
        self.show_m = None
        self.panel = None

    def load_tractogram(self):
        tractogram = load_tractogram(self.trk_file, "same")
        self.streamlines = tractogram.streamlines
        self.data = tractogram.data_per_point
        self.affine = tractogram.affine
        self.shape = self.data.shape

    def setup_scene(self):
        stream_actor = actor.line(self.streamlines)
        image_actor_z = actor.slicer(self.data, affine=self.affine)
        slicer_opacity = 0.6
        image_actor_z.opacity(slicer_opacity)

        image_actor_x = image_actor_z.copy()
        x_midpoint = int(np.round(self.shape[0] / 2))
        image_actor_x.display_extent(
            x_midpoint, x_midpoint, 0, self.shape[1] - 1, 0, self.shape[2] - 1
        )

        image_actor_y = image_actor_z.copy()
        y_midpoint = int(np.round(self.shape[1] / 2))
        image_actor_y.display_extent(
            0, self.shape[0] - 1, y_midpoint, y_midpoint, 0, self.shape[2] - 1
        )

        self.scene.add(stream_actor)
        self.scene.add(image_actor_z)
        self.scene.add(image_actor_x)
        self.scene.add(image_actor_y)

        self.show_m = window.ShowManager(scene=self.scene, size=(1200, 900))
        self.show_m.initialize()

        line_slider_z = ui.LineSlider2D(
            min_value=0,
            max_value=self.shape[2] - 1,
            initial_value=self.shape[2] / 2,
            text_template="{value:.0f}",
            length=140,
        )

        line_slider_x = ui.LineSlider2D(
            min_value=0,
            max_value=self.shape[0] - 1,
            initial_value=self.shape[0] / 2,
            text_template="{value:.0f}",
            length=140,
        )

        line_slider_y = ui.LineSlider2D(
            min_value=0,
            max_value=self.shape[1] - 1,
            initial_value=self.shape[1] / 2,
            text_template="{value:.0f}",
            length=140,
        )

        opacity_slider = ui.LineSlider2D(
            min_value=0.0, max_value=1.0, initial_value=slicer_opacity, length=140
        )

        def change_slice_z(slider):
            z = int(np.round(slider.value))
            image_actor_z.display_extent(
                0, self.shape[0] - 1, 0, self.shape[1] - 1, z, z
            )

        def change_slice_x(slider):
            x = int(np.round(slider.value))
            image_actor_x.display_extent(
                x, x, 0, self.shape[1] - 1, 0, self.shape[2] - 1
            )

        def change_slice_y(slider):
            y = int(np.round(slider.value))
            image_actor_y.display_extent(
                0, self.shape[0] - 1, y, y, 0, self.shape[2] - 1
            )

        def change_opacity(slider):
            slicer_opacity = slider.value
            image_actor_z.opacity(slicer_opacity)
            image_actor_x.opacity(slicer_opacity)
            image_actor_y.opacity(slicer_opacity)

        line_slider_z.on_change = change_slice_z
        line_slider_x.on_change = change_slice_x
        line_slider_y.on_change = change_slice_y
        opacity_slider.on_change = change_opacity

        def build_label(text):
            label = ui.TextBlock2D()
            label.message = text
            label.font_size = 18
            label.font_family = "Arial"
            label.justification = "left"
            label.bold = False
            label.italic = False
            label.shadow = False
            label.background_color = (0, 0, 0)
            label.color = (1, 1, 1)
            return label

        line_slider_label_z = build_label(text="Z Slice")
        line_slider_label_x = build_label(text="X Slice")
        line_slider_label_y = build_label(text="Y Slice")
        opacity_slider_label = build_label(text="Opacity")

        self.panel = ui.Panel2D(
            size=(300, 200), color=(1, 1, 1), opacity=0.1, align="right"
        )
        self.panel.center = (1030, 120)

        self.panel.add_element(line_slider_label_x, (0.1, 0.75))
        self.panel.add_element(line_slider_x, (0.38, 0.75))
        self.panel.add_element(line_slider_label_y, (0.1, 0.55))
        self.panel.add_element(line_slider_y, (0.38, 0.55))
        self.panel.add_element(line_slider_label_z, (0.1, 0.35))
        self.panel.add_element(line_slider_z, (0.38, 0.35))
        self.panel.add_element(opacity_slider_label, (0.1, 0.15))
        self.panel.add_element(opacity_slider, (0.38, 0.15))

        self.scene.add(self.panel)

        global size
        size = self.scene.GetSize()

        def win_callback(obj, event):
            global size
            if size != obj.GetSize():
                size_old = size
                size = obj.GetSize()
                size_change = [size[0] - size_old[0], 0]
                self.panel.re_align(size_change)

        self.show_m.add_window_callback(win_callback)

    def show(self, interactive=True):
        self.scene.zoom(1.5)
        self.scene.reset_clipping_range()

        if interactive:
            self.show_m.render()
            self.show_m.start()
        else:
            window.record(
                scene=self.scene,
                out_path="bundles_and_3_slices.png",
                size=(1200, 900),
                reset_camera=False,
            )


# Example usage
if __name__ == "__main__":
    visualizer = StreamlineVisualizer("path_to_your_streamlines.trk")
    visualizer.load_tractogram()
    visualizer.setup_scene()
    visualizer.show(interactive=True)
