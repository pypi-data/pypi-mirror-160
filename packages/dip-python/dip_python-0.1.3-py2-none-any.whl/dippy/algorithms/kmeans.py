import numpy as np


def kmeans(src: np.ndarray, N: int = 16) -> np.ndarray:
    dst = src.copy()
    represents = np.random.randint(256, size=(N))
    for _ in range(10):
        distortions = [[0, 0] for _ in range(N)]
        for y in range(src.shape[1]):
            for x in range(src.shape[0]):
                idx = np.argmin(np.abs(represents-dst[y][x]))
                distortions[idx][0] += dst[y][x]
                distortions[idx][1] += 1
                dst[y][x] = represents[idx]
        represents = np.array([distortions[i][0]/(distortions[i][1]+1e-12) for i in range(N)])
    return dst.astype(np.uint8)
