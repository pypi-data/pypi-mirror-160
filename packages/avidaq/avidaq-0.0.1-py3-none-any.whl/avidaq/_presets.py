from typing import TypedDict

import numpy.typing as npt

__all__ = ["IMDAParams", "MDAPresets", "get_mda_presets"]


class IMDAParams(TypedDict, total=False):
    """Inputs for the multi-dimensional acquisition events."""

    num_time_points: int
    time_interval_s: float
    z_start: float
    z_end: float
    z_step: float
    channel_group: str
    channels: list
    channel_exposures_ms: list
    xy_positions: npt.ArrayLike
    xyz_positions: npt.ArrayLike
    order: str
    keep_shutter_open_between_channels: bool
    keep_shutter_open_between_z_steps: bool


class MDAPresets(TypedDict):
    Default: IMDAParams
    Simple: IMDAParams
    Detailed: IMDAParams


def get_mda_presets() -> MDAPresets:
    return MDAPresets(
        Default=IMDAParams(
            num_time_points=5,
            z_start=0,
            z_end=6,
            z_step=0.4,
        ),
        Simple=IMDAParams(
            num_time_points=2,
            z_start=0,
            z_end=2,
            z_step=0.1,
        ),
        Detailed=IMDAParams(
            num_time_points=10,
            z_start=0,
            z_end=12,
            z_step=0.2,
        ),
    )
