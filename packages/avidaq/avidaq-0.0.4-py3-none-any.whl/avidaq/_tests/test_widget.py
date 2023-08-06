from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np

from avidaq import ExampleQWidget

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from napari import Viewer

    ViewerFactory = Callable[[], Viewer]


# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
def test_example_q_widget(
    make_napari_viewer: ViewerFactory, capsys: CaptureFixture
) -> None:
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((100, 100)))

    # create our widget, passing in the viewer
    my_widget = ExampleQWidget(viewer)

    # call our widget method
    my_widget.receive_data(np.random.random((100, 100)))

    # read captured output and check that it's as we expected
    captured = capsys.readouterr()
    assert captured.out == "napari has 2 layers\n"
