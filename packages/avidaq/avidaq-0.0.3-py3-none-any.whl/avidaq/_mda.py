from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

import numpy.typing as npt

__all__ = ["IMDAParams", "MDAPresets", "get_mda_presets", "MDA"]


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


@dataclass
class MDA:
    save_path: Path = Path().home() / ".avidaq" / "mda_presets.json"

    @property
    def paramsets(self) -> MDAPresets | dict[str, IMDAParams]:
        if not self.save_path.exists():
            print(f"{self.save_path} does not exist. Creating it.")
            self.save_path.touch()
            self.save_path.write_text(json.dumps(get_mda_presets(), indent=2))

        with open(self.save_path, "r+") as f:
            try:
                paramsets = json.load(f)
            except json.JSONDecodeError as e:
                print(e)
                paramsets = get_mda_presets()
                f.write(json.dumps(paramsets, indent=2))
            return paramsets

    @paramsets.setter
    def paramsets(self, paramsets: dict[str, IMDAParams]) -> None:
        with open(self.save_path, "w") as f:
            f.write(json.dumps(paramsets, indent=2))


if __name__ == "__main__":
    mda = MDA()
    print(mda.paramsets)
