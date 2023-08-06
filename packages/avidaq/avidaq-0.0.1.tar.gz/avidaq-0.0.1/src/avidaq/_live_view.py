from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from qtpy.QtCore import QObject, QRunnable, Signal, Slot

from ._utils import fix_tagged_shape

if TYPE_CHECKING:
    from ._widget import ExampleQWidget


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    :param data: A Signal for sending data from the worker to the main thread.
    :param progress: A Signal for sending progress updates to the main thread.
    """

    data = Signal(np.ndarray)
    is_active = Signal(bool)


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
        print("Starting live view")
        core = self.parent.core
        frame_rate = int(1000 / 24)

        try:
            self.parent.core.start_continuous_sequence_acquisition(frame_rate)
        except Exception as e:
            print(e)

        while self.parent.live_view_push_button.isChecked():
            try:
                image = fix_tagged_shape(core.get_last_tagged_image())
                self.signals.data.emit(image)
            except Exception as e:
                print(type(e))

        print("Stopping live view")
