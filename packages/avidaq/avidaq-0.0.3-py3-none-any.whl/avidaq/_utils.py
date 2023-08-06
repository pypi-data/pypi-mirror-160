import numpy as np
import numpy.typing as npt

from ._types import PMMCoreJTaggedImage


def fix_tagged_shape(
    tagged_image: PMMCoreJTaggedImage,
) -> npt.NDArray[np.uint16]:
    """Convert a 1D tagged image into a 2D numpy image."""
    return np.reshape(
        tagged_image.pix,
        newshape=(tagged_image.tags["Height"], tagged_image.tags["Width"]),
    )
