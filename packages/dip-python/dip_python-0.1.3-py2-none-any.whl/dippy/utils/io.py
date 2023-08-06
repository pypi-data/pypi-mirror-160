import zlib


def readBmp(path: str):
    with open(path, "rb") as f:
        # BMP file header
        f.read(2)  # bfType
        f.read(4)  # bfSize         = int.from_bytes(f.read(4), byteorder='little')
        f.read(2)  # bfReserved1    = int.from_bytes(f.read(2), byteorder='little')
        f.read(2)  # bfReserved2    = int.from_bytes(f.read(2), byteorder='little')
        bfOffBits = int.from_bytes(f.read(4), byteorder='little')

        # BMP information header
        f.read(4)  # bcSize         = int.from_bytes(f.read(4), byteorder='little')
        bcWidth = int.from_bytes(f.read(4), byteorder='little')
        bcHeight = int.from_bytes(f.read(4), byteorder='little')
        f.read(2)  # bcPlanes       = int.from_bytes(f.read(2), byteorder='little')
        bcBitCount = int.from_bytes(f.read(2), byteorder='little')
        f.read(4)  # biCompression  = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biSizeImage    = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biXPixPerMeter = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biYPixPerMeter = int.from_bytes(f.read(4), byteorder='little')
        biClrUsed = int.from_bytes(f.read(4), byteorder='little')
        f.read(4)  # biCirImportant = int.from_bytes(f.read(4), byteorder='little')

        colorTable = f.read(biClrUsed << 2)
        _ = f.read(bfOffBits - (0x0e + 0x28 + (biClrUsed << 2)))
        pixels = f.read()

        return bcWidth, bcHeight, bcBitCount, colorTable, pixels


def readPng(path: str):
    with open(path, "rb") as f:
        # PNG header
        f.read(8)  # pngSignature = int.from_bytes(f.read(8), byteorder='big')

        # IHDR chunk
        f.read(4)  # chLength     = int.from_bytes(f.read(4), byteorder='big')
        f.read(4)  # chType       = int.from_bytes(f.read(4), byteorder='big')
        width = int.from_bytes(f.read(4), byteorder='big')
        height = int.from_bytes(f.read(4), byteorder='big')
        depth = int.from_bytes(f.read(1), byteorder='big')
        colorType = int.from_bytes(f.read(1), byteorder='big')
        f.read(1)  # compression  = int.from_bytes(f.read(1), byteorder='big')
        f.read(1)  # filter       = int.from_bytes(f.read(1), byteorder='big')
        interlace = int.from_bytes(f.read(1), byteorder='big')
        f.read(4)  # CRC          = int.from_bytes(f.read(4), byteorder='big')

        # Other chunks
        offset = 0
        cmp_data = []
        while True:
            length = int.from_bytes(f.read(4), byteorder='big')
            chunkType = f.read(4).decode()
            if chunkType == "IDAT":
                cmp_data[offset:] = f.read(length)
                f.read(4)  # CRC
                offset += length
            elif chunkType == "IEND":
                break
            else:
                f.read(length)
                f.read(4)  # CRC

        # Decompress data
        decmp_data = zlib.decompress(bytearray(cmp_data))

        # Apply filter
        if colorType == 0:
            bitsPerPixel = depth
        elif colorType == 2:
            bitsPerPixel = depth * 3
        elif colorType == 3:
            bitsPerPixel = depth
        elif colorType == 4:
            bitsPerPixel = depth * 2
        elif colorType == 6:
            bitsPerPixel = depth
        rowLength = int(1 + (bitsPerPixel * width + 7) / 8)
        filtered_data = []
        rowData = []
        prevRowData = [0 for _ in range(rowLength)]
        bytesPerPixel = int((bitsPerPixel + 7) / 8)
        for h in range(height):
            offset = h * rowLength
            rowData[0:] = decmp_data[offset:offset+rowLength]
            filterType = int(rowData[0])

            currentScanData = rowData[1:].copy()
            prevScanData = prevRowData[1:].copy()

            if filterType == 0:
                pass
            elif filterType == 1:
                for i in range(0, len(currentScanData)):
                    if (i - bytesPerPixel) < 0:
                        currentScanData[i] += 0
                    else:
                        currentScanData[i] += currentScanData[i-bytesPerPixel]
                    currentScanData[i] %= 256
            elif filterType == 2:
                for i in range(0, len(currentScanData)):
                    currentScanData[i] += prevScanData[i]
                    currentScanData[i] %= 256
            elif filterType == 3:
                for i in range(0, bytesPerPixel):
                    currentScanData[i] += int(prevScanData[i] / 2)
                    currentScanData[i] %= 256
                for i in range(bytesPerPixel, len(currentScanData)):
                    if (i - bytesPerPixel) < 0:
                        tmp = int(prevScanData[i] / 2)
                    else:
                        tmp = int((currentScanData[i-bytesPerPixel]+prevScanData[i]) / 2)
                    currentScanData[i] += tmp
                    currentScanData[i] %= 256
            elif filterType == 4:
                for i in range(0, bytesPerPixel):
                    a = 0
                    c = 0
                    for j in range(i, len(currentScanData), bytesPerPixel):
                        b = prevScanData[j]
                        pa = b - c
                        pb = a - c
                        pc = abs(pa + pb)
                        pa = abs(pa)
                        pb = abs(pb)
                        if (pa <= pb) and (pa <= pc):
                            pass
                        elif pb <= pc:
                            a = b
                        else:
                            a = c
                        a += currentScanData[j]
                        a &= 0xff
                        currentScanData[j] = a % 256
                        c = b
            else:
                # Bad Filter Type Error
                pass
            filtered_data[h*len(currentScanData):] = currentScanData.copy()
            prevRowData[0:] = rowData[0:1]
            prevRowData[1:] = currentScanData.copy()

        return width, height, depth, colorType, interlace, bytearray(filtered_data)


def writeBmp(path: str, width: int, height: int, bitCount: int, colorTables, pixels):
    with open(path, 'wb') as f:
        lenOfColors = len(colorTables)
        numOfColors = lenOfColors >> 2
        if (bitCount >> 3) == 1:
            color = [(i // 4 if (i % 4) != 0 else 0) for i in range(1, 1025)]
        else:
            color = None
        try:
            lenOfColor = len(color)
        except TypeError:
            lenOfColor = 0
        bfOffBits = 0x0e + 0x28 + lenOfColors + lenOfColor
        lenOfPixels = len(pixels)
        fileSize = bfOffBits + lenOfPixels

        # BMP file header
        b = bytearray([0x42, 0x4d])
        b.extend(fileSize.to_bytes(4, 'little'))
        b.extend((0).to_bytes(2, 'little'))
        b.extend((0).to_bytes(2, 'little'))
        b.extend(bfOffBits.to_bytes(4, 'little'))

        # BMP information header
        b.extend((0x28).to_bytes(4, 'little'))
        b.extend(width.to_bytes(4, 'little'))
        b.extend(height.to_bytes(4, 'little'))
        b.extend((1).to_bytes(2, 'little'))
        b.extend((bitCount).to_bytes(2, 'little'))
        b.extend((0).to_bytes(4, 'little'))
        b.extend(lenOfPixels.to_bytes(4, 'little'))
        b.extend((0).to_bytes(4, 'little'))
        b.extend((0).to_bytes(4, 'little'))
        b.extend(numOfColors.to_bytes(4, 'little'))
        b.extend((0).to_bytes(4, 'little'))

        b.extend(colorTables)
        try:
            b.extend(bytearray(color))
        except TypeError:
            pass
        b.extend(pixels)

        f.write(b)


def writePng(path: str, width: int, height: int, depth: int, colorType: int, interlace: int, pixels):
    with open(path, 'wb') as f:
        # PNG signature
        b = bytearray([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])

        # IHDR
        b.extend((13).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "IHDR"]))
        # b.extend(bytearray([0x49, 0x48, 0x44, 0x52]))
        b.extend(width.to_bytes(4, 'big'))
        b.extend(height.to_bytes(4, 'big'))
        b.extend(depth.to_bytes(1, 'big'))
        b.extend(colorType.to_bytes(1, 'big'))
        b.extend((0).to_bytes(1, 'big'))
        b.extend((0).to_bytes(1, 'big'))
        b.extend(interlace.to_bytes(1, 'big'))
        b.extend(bytearray([0x7b, 0x1a, 0x43, 0xad]))

        # sRGB
        b.extend((1).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "sRGB"]))
        # b.extend(bytearray([0x73, 0x52, 0x47, 0x42]))
        b.extend(bytearray([0x00]))
        b.extend(bytearray([0xae, 0xce, 0x1c, 0xe9]))

        # IDAT
        data = []
        for h in range(height):
            offset = h * (width*3)
            # data[offset:] = [0]
            data.append(0)
            data[offset+h+1:] = pixels[offset:offset+width*3]
        cmp_data = zlib.compress(bytearray(data))

        b.extend(len(cmp_data).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "IDAT"]))
        b.extend(cmp_data)
        b.extend(bytearray([0xa5, 0x46, 0x15, 0x38]))

        # IEND
        b.extend((0).to_bytes(4, 'big'))
        b.extend(bytearray([ord(x) for x in "IEND"]))
        b.extend(bytearray([0xae, 0x42, 0x60, 0x82]))

        f.write(b)
