# PBM format
# https://netpbm.sourceforge.net/doc/pbm.html

DIGITS = {
    0: [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]],
    1: [[0, 0, 1, 0, 0], [0, 1, 1, 0, 0], [1, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1]],
    2: [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 1, 1]],
    3: [[1, 1, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 1, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [1, 1, 1, 1, 0]],
    4: [[0, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [1, 0, 0, 1, 0], [1, 1, 1, 1, 1], [0, 0, 0, 1, 0], [0, 0, 1, 1, 1]],
    5: [[1, 1, 1, 1, 1], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [1, 1, 1, 1, 0]],
    6: [[0, 0, 1, 1, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]],
    7: [[1, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 0, 0]],
    8: [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]],
    9: [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 1, 1, 1, 0]],
}


def draw(filename: str, width: int, height: int, pixels: list, timestamp: int):
    with open(filename, "w") as img:
        rh = height + 9 + (1 - height % 2) * 1  # this will make even number of pixels for ffmpeg
        rw = width + width % 2  # this will make even number of pixels for ffmpeg
        pad = (rw // 7) - 1  # pad timestamp with zeroes
        img.write("P1\n")
        img.write(f"{width} {rh}\n")
        # initialize matrix with all zeroes
        matrix = []
        for _ in range(rh):
            matrix.append([0] * width)
        # pixels is a list of tuples for pixel to be "ON" in format (x,y)
        for px, py in pixels:
            matrix[py][px] = 1
        # write timestamp at bottom line, spaced by one pixel
        for position, digit in enumerate(str(timestamp).zfill(pad)):
            for dy in range(7):
                for dx in range(5):
                    y = height + 1 + dy
                    x = 1 + dx + position * 7
                    matrix[y][x] = DIGITS[int(digit)][dy][dx]
        # write image to disk
        for line in matrix:
            img.write("".join(str(pixel) for pixel in line) + "\n")
