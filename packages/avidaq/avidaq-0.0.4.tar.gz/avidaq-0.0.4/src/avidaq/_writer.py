"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/plugins/guides.html?#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Protocol,
    Sequence,
    Tuple,
    TypedDict,
    Union,
)

import numpy as np
import numpy.typing as npt
from pycromanager import Core

__all__ = [
    "get_image",
]


class PTaggedImageDict(TypedDict):
    Height: int
    Width: int


class PTaggedImage(Protocol):
    pix: npt.NDArray
    tags: PTaggedImageDict


if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]


def write_single_image(path: str, data: Any, meta: dict):
    """Writes a single image layer"""


def write_multiple(path: str, data: List[FullLayerData]):
    """Writes multiple layers of different types."""


def get_image() -> npt.NDArray:

    core = Core()  # type: ignore
    core.set_property("Core", "AutoShutter", 0)  # type: ignore
    core.snap_image()  # type: ignore
    tagged_image: PTaggedImage = core.get_tagged_image()  # type: ignore

    # pixels by default come out as a 1D array.
    # We can reshape them into an image
    pixels = np.reshape(
        tagged_image.pix,
        newshape=(
            tagged_image.tags["Height"],
            tagged_image.tags["Width"],
        ),
    )

    return pixels

    # if data is None:
    #     try:
    #         data = self._mmc.getLastImage()
    #     except (RuntimeError, IndexError):
    #         # circular buffer empty
    #         return
