""" This module contains functions for dealing with image data."""
from __future__ import annotations

import shutil
from collections.abc import Iterator
from pathlib import Path

__all__ = ["get_image_directories", "delete_image_data"]


def get_image_directories(*, base_path: Path, name: str) -> Iterator[Path]:
    """
    Args:
        base_path (Path): Where to start looking for image directories.
        target (str): The name that was given to micromanager to create
        the image directories.

    Yields:
        Iterator[Path]: directories of where a named image is stored
    """
    return (
        entry
        for entry in base_path.glob("*")
        if name in entry.stem and entry.is_dir()
    )


def delete_image_data(image_directories: Iterator[Path]) -> None:
    for directory in image_directories:
        shutil.rmtree(directory)
