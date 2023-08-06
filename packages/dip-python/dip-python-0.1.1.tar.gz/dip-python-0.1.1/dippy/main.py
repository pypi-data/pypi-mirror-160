import time
import dippy as dp


def main():
    start = time.perf_counter()

    path = "../data/color/Lenna.bmp"
    # path = "../data/mono/LENNA.bmp"
    w, h, bc, ct, bimg = dp.readBmp(path)

    isColor = True if ((bc >> 3) == 3) else False
    ndimg = dp.b2ndarray(bimg, w, h, isColor)
    # ndimg = dp.reverseNP(ndimg)
    # ndimg = dp.convertColor(ndimg, "rgb2gray")
    # ndimg = dp.binarize(ndimg, "otsu")
    # ndimg = dp.posterization(ndimg, "equality")
    # ndimg = dp.dithering(ndimg, method="bayer")
    # ndimg = dp.kmeans(ndimg)
    bimg, bc = dp.ndarray2b(ndimg)
    dp.writeBmp("../data/dst.bmp", w, h, bc, ct, bimg)

    path = "../data/Lenna.png"
    w, h, d, cType, interlace, bimg = dp.readPng(path)
    ndimg = dp.b2ndarray(bimg, w, h, isColor)
    ndimg = ndimg[[2, 1, 0], :, ::-1]
    ndimg = dp.convertColor(ndimg, "rgb2gray")
    ndimg = dp.dithering(ndimg, method="bayer")
    bimg, bc = dp.ndarray2b(ndimg)
    dp.writeBmp("../data/png.bmp", w, h, bc, ct, bimg)
    ndimg = ndimg[[2, 1, 0], :, ::-1]
    bimg, bc = dp.ndarray2b(ndimg)
    dp.writePng("../data/dst.png", w, h, d, cType, interlace, bimg)

    end = time.perf_counter()
    print(f"time:{end - start}")


if __name__ == "__main__":
    main()
