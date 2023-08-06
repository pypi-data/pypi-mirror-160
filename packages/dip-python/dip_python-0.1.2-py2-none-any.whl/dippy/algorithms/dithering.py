import numpy as np


def neighbor(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        for x in range(0, src.shape[0]):
            if dst[y][x] < 127.5:
                err = dst[y][x] - 0
                dst[y][x] = 0
            else:
                err = dst[y][x] - 255
                dst[y][x] = 255
            if (x + 1) < src.shape[0]:
                dst[y][x+1] += err
    return dst.astype(np.uint8)


def neighbor_2way(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        if (y % 2) == 0:
            for x in range(0, src.shape[0]):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x + 1) < src.shape[0]:
                    dst[y][x+1] += err
        else:
            for x in range(src.shape[0], 0):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x - 1) > 0:
                    dst[y][x-1] += err
    return dst.astype(np.uint8)


def floyd_steinberg(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        for x in range(0, src.shape[0]):
            if dst[y][x] < 127.5:
                err = dst[y][x] - 0
                dst[y][x] = 0
            else:
                err = dst[y][x] - 255
                dst[y][x] = 255
            if (x + 1) < src.shape[0]:
                dst[y][x+1] += err * (7 / 16)
            if ((x - 1) > 0) and ((y + 1) < src.shape[1]):
                dst[y+1][x-1] += err * (3 / 16)
            if (y + 1) < src.shape[1]:
                dst[y+1][x] += err * (5 / 16)
            if ((x + 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                dst[y+1][x+1] += err * (1 / 16)
    return dst.astype(np.uint8)


def floyd_steinberg_2way(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        if (y % 2) == 0:
            for x in range(0, src.shape[0]):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x + 1) < src.shape[0]:
                    dst[y][x+1] += err * (7 / 16)
                if ((x - 1) > 0) and ((y + 1) < src.shape[1]):
                    dst[y+1][x-1] += err * (3 / 16)
                if (y + 1) < src.shape[1]:
                    dst[y+1][x] += err * (5 / 16)
                if ((x + 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                    dst[y+1][x+1] += err * (1 / 16)
        else:
            for x in range(src.shape[0], 0):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x - 1) > 0:
                    dst[y][x-1] += err * (7 / 16)
                if ((x + 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                    dst[y+1][x+1] += err * (3 / 16)
                if (y + 1) < src.shape[1]:
                    dst[y+1][x] += err * (5 / 16)
                if ((x - 1) > 0) and ((y + 1) < src.shape[1]):
                    dst[y+1][x-1] += err * (1 / 16)
    return dst.astype(np.uint8)


def sierra_lite(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        for x in range(0, src.shape[0]):
            if dst[y][x] < 127.5:
                err = dst[y][x] - 0
                dst[y][x] = 0
            else:
                err = dst[y][x] - 255
                dst[y][x] = 255
            if (x + 1) < src.shape[0]:
                dst[y][x+1] += (err / 4) * 2
            if ((x - 1) > 0) and ((y + 1) < src.shape[1]):
                dst[y+1][x-1] += err / 4
            if (y + 1) < src.shape[1]:
                dst[y+1][x] += err / 4
    return dst.astype(np.uint8)


def sierra_lite_2way(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        if (y % 2) == 0:
            for x in range(0, src.shape[0]):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x + 1) < src.shape[0]:
                    dst[y][x+1] += (err / 4) * 2
                if ((x - 1) > 0) and ((y + 1) < src.shape[1]):
                    dst[y+1][x-1] += err / 4
                if (y + 1) < src.shape[1]:
                    dst[y+1][x] += err / 4
        else:
            for x in range(src.shape[0], 0):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x - 1) > 0:
                    dst[y][x-1] += (err / 4) * 2
                if ((x + 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                    dst[y+1][x+1] += err / 4
                if (y + 1) < src.shape[1]:
                    dst[y+1][x] += err / 4
    return dst.astype(np.uint8)


def atkinson(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        for x in range(0, src.shape[0]):
            if dst[y][x] < 127.5:
                err = dst[y][x] - 0
                dst[y][x] = 0
            else:
                err = dst[y][x] - 255
                dst[y][x] = 255
            if (x + 2) < src.shape[0]:
                dst[y][x+2] += err / 8
            if (x + 1) < src.shape[0]:
                dst[y][x+1] += err / 8
            if ((x - 1) > 0) and ((y + 1) < src.shape[1]):
                dst[y+1][x-1] += err / 8
            if (y + 1) < src.shape[1]:
                dst[y+1][x] += err / 8
            if ((x + 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                dst[y+1][x+1] += err / 8
            if (y + 2) < src.shape[1]:
                dst[y+2][x] += err / 8
    return dst.astype(np.uint8)


def atkinson_2way(src: np.ndarray) -> np.ndarray:
    dst = src.copy()
    for y in range(src.shape[1]):
        if (y % 2) == 0:
            for x in range(0, src.shape[0]):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x + 2) < src.shape[0]:
                    dst[y][x+2] += err / 8
                if (x + 1) < src.shape[0]:
                    dst[y][x+1] += err / 8
                if ((x - 1) > 0) and ((y + 1) < src.shape[1]):
                    dst[y+1][x-1] += err / 8
                if (y + 1) < src.shape[1]:
                    dst[y+1][x] += err / 8
                if ((x + 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                    dst[y+1][x+1] += err / 8
                if (y + 2) < src.shape[1]:
                    dst[y+2][x] += err / 8
        else:
            for x in range(src.shape[0], 0):
                if dst[y][x] < 127.5:
                    err = dst[y][x] - 0
                    dst[y][x] = 0
                else:
                    err = dst[y][x] - 255
                    dst[y][x] = 255
                if (x - 2) > 0:
                    dst[y][x-2] += err / 8
                if (x - 1) > 0:
                    dst[y][x-1] += err / 8
                if ((x + 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                    dst[y+1][x+1] += err / 8
                if (y + 1) < src.shape[1]:
                    dst[y+1][x] += err / 8
                if ((x - 1) < src.shape[0]) and ((y + 1) < src.shape[1]):
                    dst[y+1][x-1] += err / 8
                if (y + 2) < src.shape[1]:
                    dst[y+2][x] += err / 8
    return dst.astype(np.uint8)


def dithering(src: np.ndarray, method: str = "random") -> np.ndarray:
    if method == "random":
        dst = np.vectorize(lambda x: 255 if (np.random.rand() < (x/255)) else 0)(src)
    elif method == "bayer":
        dst = src.copy()
        mat = np.array([[0, 2], [3, 1]])
        # mat = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
        # mat = np.array([[10, 4, 6, 8], [12, 0, 2, 14], [7, 9, 11, 5], [3, 15, 13, 1]])
        # mat = np.array([[13, 7, 6, 12], [8, 1, 0, 5], [9, 2, 3, 4], [14, 10, 11, 15]])
        for y in range(src.shape[1] // mat.shape[1]):
            for x in range(src.shape[0] // mat.shape[0]):
                for i in range(mat.shape[1]):
                    for j in range(mat.shape[0]):
                        if dst[(y*mat.shape[1])+j][(x*mat.shape[0])+i] > (mat[j][i] * (255 / (mat.shape[0]*mat.shape[1]))):
                            dst[(y*mat.shape[1])+j][(x*mat.shape[0])+i] = 255
                        else:
                            dst[(y*mat.shape[1])+j][(x*mat.shape[0])+i] = 0
    elif method == "neighbor":
        dst = neighbor(src)
    elif method == "floyd_steinberg":
        dst = floyd_steinberg(src)
    elif method == "sierra_lite":
        dst = sierra_lite(src)
    elif method == "atkinson":
        dst = atkinson(src)
    return dst.astype(np.uint8)


def dithering_2way(src: np.ndarray, method: str = "random") -> np.ndarray:
    if method == "neighbor":
        dst = neighbor_2way(src)
    elif method == "floyd_steinberg":
        dst = floyd_steinberg_2way(src)
    elif method == "sierra_lite":
        dst = sierra_lite_2way(src)
    elif method == "atkinson":
        dst = atkinson_2way(src)
    return dst.astype(np.uint8)
