import numpy as np
np.seterr(divide='ignore', invalid='ignore')


def reverseNP(src: np.ndarray) -> np.ndarray:
    dst = 255 - src
    return dst


def convertColor(src: np.ndarray, method: str = "rgb2gray") -> np.ndarray:
    if len(src.shape) == 3:
        if method == "rgb2gray":
            dst = np.apply_along_axis(
                lambda x: 0.299*x[0] + 0.587*x[1] + 0.114*x[2],
                # lambda x: 0.333*x[0] + 0.333*x[1] + 0.333*x[2],
                0,
                src)
        elif method == "rgb2bgr":
            dst = src[[2, 1, 0], :, :]
    return dst.astype(np.uint8)


def binarize(src: np.ndarray, method: str = "threshold", threshold: int = 128) -> np.ndarray:
    if method == "threshold":
        lut = np.zeros((256))
        lut[threshold:] = 255
    elif method == "otsu":
        s = []
        p_all = np.sum(src)
        offset = 21
        for i in range(0+offset, 256-offset):
            M = np.average(src[src < i]) - np.average(src[src >= i])
            s.append(
                (np.sum(src[src < i]) / p_all)
                * (np.sum(src[src >= i]) / p_all)
                * M
                * M)
        threshold = np.nanargmax(s)
        lut = np.zeros((256))
        lut[threshold:] = 255
    dst = lut[src]
    return dst.astype(np.uint8)


def posterization(src: np.ndarray, method: str = "nearest_neighbor", tone=8) -> np.ndarray:
    lut = np.zeros((256))
    if method == "nearest_neighbor":
        tmp = 255 / ((tone - 1) * 2)
        for t in range(1, tone):
            lut[int(tmp*(2*t-1)):] = int((255/(tone-1)) * t)
    elif method == "equality":
        for t in range(1, tone):
            lut[int((255/tone)*t):] = int((255/(tone-1)) * t)
    dst = lut[src]
    return dst.astype(np.uint8)
