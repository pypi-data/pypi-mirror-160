import numpy as np
from typing import Tuple


def b2ndarray(bimg: bytes, width: int, height: int, isColor: bool) -> np.ndarray:
    ndimg = (np.frombuffer(bimg, dtype=np.uint8))
    if isColor:
        ndimg = ndimg.reshape([3, width, height], order='F').copy()
        ndimg = ndimg[[2, 1, 0], ::-1, :]
    else:
        ndimg = ndimg.reshape([width, height], order='F').copy()
        ndimg = ndimg[::-1, :]
    return ndimg


def ndarray2b(ndimg: np.ndarray) -> Tuple[bytes, int]:
    if len(ndimg.shape) == 3:
        ndimg = ndimg[[2, 1, 0], ::-1, :]
        bimg = ndimg.reshape(-1, order='F').copy().tobytes()
        bc = 0x08 * 3
    else:
        ndimg = ndimg[::-1, :]
        bimg = ndimg.reshape(-1, order='F').copy().tobytes()
        bc = 0x08
    return bimg, bc
