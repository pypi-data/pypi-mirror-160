from __future__ import annotations

from pathlib import Path

import pytest

from avidaq._mda import get_mda_presets


def test_empty_json_file() -> None:

    # delete the file
    try:
        Path("mda_presets.json").unlink()
    except (FileNotFoundError):
        pass
    Path("mda_presets.json").touch()

    with pytest.raises(ValueError):
        file_data = get_mda_presets()
        assert file_data == {}
