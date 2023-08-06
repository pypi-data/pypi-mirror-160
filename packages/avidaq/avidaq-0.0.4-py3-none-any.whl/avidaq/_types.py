from __future__ import annotations

from typing import Literal, Protocol, TypedDict

import numpy as np
import numpy.typing as npt

__all__ = ["PCore", "TaggedImageTags", "PMMCoreJTaggedImage"]


class PCore(Protocol):
    """Methods for pycromanager `Core` object.

    This exists because intellisense won't shown the methods available to core
    since they aren't known until runtime.

    Derived from:
    https://valelab4.ucsf.edu/~MM/doc/MMCore/html/class_c_m_m_core.html
    """

    def set_xy_position(self, x: float, y: float) -> None:
        ...

    def set_relative_xy_position(self, x: float, y: float) -> None:
        ...

    def get_x_position(self) -> float:
        ...

    def get_y_position(self) -> float:
        ...

    def get_position(self) -> int | float:
        """Set z-axis position."""
        ...

    def set_relative_position(self, size: float) -> None:
        """Get the z-axis position."""
        ...

    def get_exposure(self) -> float | int:
        ...

    def set_exposure(self, value: float | int) -> None:
        ...

    def start_continuous_sequence_acquisition(self, ms_interval: int) -> None:
        ...

    def get_last_tagged_image(
        self,
    ) -> PMMCoreJTaggedImage:
        """Retrieve the last image when running in continuous
        acquisition mode."""
        ...

    def is_sequence_running(self) -> bool:
        ...

    def stop_sequence_acquisition(self) -> None:
        ...

    def home(self, stage_label: Literal["XY"] | str) -> None:
        ...

    def get_xy_stage_device(self) -> Literal["XY"] | str:
        ...


class TaggedImageTags(TypedDict):
    Height: int
    Width: int


class PMMCoreJTaggedImage(Protocol):
    pix: npt.NDArray[np.uint16]
    tags: TaggedImageTags
