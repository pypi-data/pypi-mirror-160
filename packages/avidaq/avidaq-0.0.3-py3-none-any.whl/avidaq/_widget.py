"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""

from __future__ import annotations

import enum
from pathlib import Path
from time import sleep
from typing import cast
from uuid import uuid4

import numpy as np
import numpy.typing as npt
from napari.viewer import Viewer
from pycromanager import Acquisition, Core, Dataset, multi_d_acquisition_events
from qtpy import QtWidgets as qtw
from qtpy.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal, Slot

from . import _live_view
from ._mda import MDA, IMDAParams, get_mda_presets
from ._right_panel import RightPanel
from ._types import PCore


class ExampleQWidget(qtw.QWidget, RightPanel):
    def __init__(self, napari_viewer: Viewer):
        super().__init__()
        self.setupUi(self)
        self.setMinimumWidth(600)
        self.core = cast(PCore, Core())  # type: ignore

        self.is_aborted = False

        self.streaming_timer: QTimer | None = None

        self.comboBox.addItems(MDA().paramsets)

        self.comboBox.currentIndexChanged.connect(
            lambda: print(get_mda_presets()[self.comboBox.currentText()])
        )

        xy_spinbox_fine_default = 1
        self.xy_spin_box_fine.setValue(xy_spinbox_fine_default)

        self.z_fine_step = 1
        self.z_fine_spinbox.setValue(self.z_fine_step)

        self.xy_coarse_step = 3
        self.xy_spin_box_coarse.setValue(self.xy_coarse_step)

        def move_stage(
            direction: XYDirection | ZDirection,
            size: float,
        ) -> None:

            direction_action_lookup = {
                XYDirection.UP: lambda: self.core.set_relative_xy_position(
                    0,
                    size,
                ),
                XYDirection.DOWN: lambda: self.core.set_relative_xy_position(
                    0,
                    -size,
                ),
                XYDirection.LEFT: lambda: self.core.set_relative_xy_position(
                    -size,
                    0,
                ),
                XYDirection.RIGHT: lambda: self.core.set_relative_xy_position(
                    size,
                    0,
                ),
                ZDirection.UP: lambda: self.core.set_relative_position(
                    size,
                ),
                ZDirection.DOWN: lambda: self.core.set_relative_position(
                    -size,
                ),
            }

            print(
                f"x:{self.core.get_x_position():.2f}\t"
                f"y:{self.core.get_y_position():.2f}\t"
                f"z:{self.core.get_position():.2f}"
            )

            return direction_action_lookup[direction]()

        def handle_load_click() -> None:
            self.core.home(self.core.get_xy_stage_device())
            print(
                f"x:{self.core.get_x_position():.2f}\t"
                f"y:{self.core.get_y_position():.2f}\t"
                f"z:{self.core.get_position():.2f}"
            )

        self.load_button.clicked.connect(handle_load_click)

        def handle_abort_click() -> None:
            self.is_aborted = True

        self.pushButton_2.clicked.connect(handle_abort_click)

        self.fine_xy_up_button.clicked.connect(
            lambda: move_stage(XYDirection.UP, self.xy_spin_box_fine.value())
        )

        self.pushButton_9.clicked.connect(
            lambda: move_stage(XYDirection.UP, self.xy_spin_box_coarse.value())
        )

        self.pushButton_12.clicked.connect(
            lambda: move_stage(XYDirection.LEFT, self.xy_spin_box_fine.value())
        )
        self.pushButton_13.clicked.connect(
            lambda: move_stage(
                XYDirection.LEFT, self.xy_spin_box_coarse.value()
            )
        )
        self.pushButton_7.clicked.connect(
            lambda: move_stage(XYDirection.DOWN, self.xy_spin_box_fine.value())
        )
        self.pushButton_6.clicked.connect(
            lambda: move_stage(
                XYDirection.DOWN, self.xy_spin_box_coarse.value()
            )
        )
        self.pushButton_10.clicked.connect(
            lambda: move_stage(
                XYDirection.RIGHT, self.xy_spin_box_fine.value()
            )
        )
        self.pushButton_11.clicked.connect(
            lambda: move_stage(
                XYDirection.RIGHT, self.xy_spin_box_coarse.value()
            )
        )
        self.pushButton_16.clicked.connect(
            lambda: move_stage(ZDirection.UP, self.z_fine_spinbox.value())
        )
        self.pushButton_14.clicked.connect(
            lambda: move_stage(ZDirection.DOWN, self.z_fine_spinbox.value())
        )

        self.z_coarse_step = 3
        self.spinBox_3.setValue(self.z_coarse_step)

        self.exposure_spin_box.setValue(self.core.get_exposure())

        def set_exposure(new_value: int) -> None:
            """Spinbox callback for `valueChanged` signal."""
            self.core.set_exposure(new_value)
            print("exposure set to", self.core.get_exposure())

        self.exposure_spin_box.valueChanged.connect(set_exposure)

        self.save_path = Path(__file__).parent / "images"
        self.active_directory_line_edit.setText(str(self.save_path))

        self.data = None
        self.viewer = napari_viewer

        self.threadpool = QThreadPool()

        self.scan_push_button.clicked.connect(self.execute_acquisition)

        def browse_directory() -> None:
            """Opens a file dialog to select a directory."""

            directory = qtw.QFileDialog.getExistingDirectory(
                self, "Select a directory", str(self.save_path.parent)
            )
            self.active_directory_line_edit.setText(directory)

        self.file_name = str(uuid4())
        self.active_file_line_edit.setText(self.file_name)
        self.active_file_line_edit.setReadOnly(False)

        self.active_file_line_edit.textChanged.connect(
            lambda new_value: setattr(self, "file_name", new_value)
        )

        self.directory_browse_button.clicked.connect(browse_directory)

        self.live_view_push_button.setCheckable(True)
        self.live_view_push_button.clicked.connect(self.execute_live_view)

    def active_mda_params(self) -> IMDAParams:
        """Lookup the current MDA preset from the combobox."""
        mda = MDA()
        return mda.paramsets[self.comboBox.currentText()]

    def execute_acquisition(self) -> None:
        worker = Worker(self)
        worker.signals.data.connect(self.receive_data)
        worker.signals.progress.connect(self.update_progress)
        self.threadpool.start(worker)

    def execute_live_view(self, is_checked: bool) -> None:
        worker = _live_view.Worker(self)
        worker.signals.data.connect(self.receive_data)

        if is_checked:
            self.live_view_push_button.setStyleSheet("color: red;")
            self.live_view_push_button.setText("Stop live view")
            self.threadpool.start(worker)
        else:
            self.live_view_push_button.setStyleSheet("color: white;")
            self.live_view_push_button.setText("Start live view")

    def update_progress(self, progress: int) -> None:
        """Updates the progress bar."""

        # disable button while progress is active
        self.scan_push_button.setEnabled(False)
        self.progressBar.setValue(progress)
        if progress in (0, 100):
            self.scan_push_button.setEnabled(True)
            self.progressBar.setValue(0)

    def receive_data(self, image: npt.NDArray) -> None:
        """Callback to receive the emitted image events from a pyqt
        `QRunnable` worker."""
        try:
            preview_layer = self.viewer.layers["preview"]  # type: ignore
            preview_layer.data = image
        except KeyError:
            preview_layer = self.viewer.add_image(image, name="preview")
            print("napari has", len(self.viewer.layers), "layers")


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    :param data: A Signal for sending data from the worker to the main thread.
    :param progress: A Signal for sending progress updates to the main thread.
    """

    data = Signal(np.ndarray)
    progress = Signal(int)


class Worker(QRunnable):
    """
    Worker thread

    :param args: Arguments to make available to the run code
    :param kwargs: Keywords arguments to make available to the run
    :code
    :
    """

    def __init__(self, parent: ExampleQWidget):
        super().__init__()
        self.parent = parent

        self.signals = (
            WorkerSignals()
        )  # Create an instance of our signals class.
        self.event_count = 0
        self.event_total = 0

    @Slot()
    def run(self) -> None:
        """
        Initialize the runner function with passed self.args,
        self.kwargs.
        """

        def on_image_saved(axes: dict[str, int], dataset: Dataset) -> None:
            """Callback for when pycromanager saves an image.

            - Emits a data(image) event event signal.
            - Emits a progress(int) event signal.

            To be passed to the Acquisition `img_save_fn` callback.
            """
            self.event_count += 1
            print(self.event_count)

            if self.parent.is_aborted is True:
                self.parent.core.stop_sequence_acquisition()
                self.signals.progress.emit(0)
                return

            sleep(0.1)
            self.signals.progress.emit(
                int(self.event_count / self.event_total * 100)
            )
            image = dataset.read_image(**axes)
            self.signals.data.emit(image)

        try:
            self.parent.core.stop_sequence_acquisition()
        except Exception as e:
            print(e)

        self.parent.is_aborted = False

        with Acquisition(
            directory=str(self.parent.save_path),
            name=self.parent.file_name,
            image_saved_fn=on_image_saved,
            show_display=False,
            debug=False,
        ) as acq:

            events = multi_d_acquisition_events(
                **self.parent.active_mda_params()
            )
            self.event_total = len(events)

            acq.acquire(events)  # type: ignore


class XYDirection(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class ZDirection(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
