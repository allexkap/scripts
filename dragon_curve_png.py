from pathlib import Path

import numpy as np
from PIL import Image

""" ./res/dragon.png
red    (255,   0,   0)  start curve point
green  (  0, 255,   0)  final curve point
black  (  0,   0,   0)  other curve points
white  (255, 255, 255)  nothing
"""


class Figure:
    rot90 = np.array(((0, -1), (1, 0)))
    dst_sign = np.array((-1, 1)).reshape(-1, 1)

    def __init__(self, field: np.ndarray, points: np.ndarray):
        self.field = field
        self.points = np.zeros((3, 2), dtype=int)
        self.points[:2, :] = points
        self.dst = np.array((points[1], np.array(field.shape) - points[1] - 1))

    def next(self):
        self.points[2] = (
            Figure.rot90 @ (self.points[0] - self.points[1]) + self.points[1]
        )
        dst_roll = np.roll(self.dst, 1)
        dst_next = np.maximum(self.dst, dst_roll)

        self.points += (dst_next - self.dst)[0]

        dst_next += Figure.dst_sign @ (self.points[1] - self.points[2]).reshape(1, -1)

        field_next = np.zeros(np.sum(dst_next, axis=0) + 1, dtype=bool)
        y0, x0 = self.points[1] - self.dst[0]
        y1, x1 = self.points[1] + self.dst[1] + 1
        field_next[y0:y1, x0:x1] = self.field
        y0, x0 = self.points[1] - dst_roll[0]
        y1, x1 = self.points[1] + dst_roll[1] + 1
        field_next[y0:y1, x0:x1] |= np.rot90(self.field)

        self.points[1] = self.points[2]
        self.dst = dst_next
        self.field = field_next

        return field_next


def crop(arr: np.ndarray):
    arr_bin = ~np.all(arr[:, :, :3], axis=2)
    minmax = lambda a: (np.min(a), np.max(a) + 1)
    x0, x1 = minmax(np.argwhere(np.any(arr_bin, axis=0)))
    y0, y1 = minmax(np.argwhere(np.any(arr_bin, axis=1)))
    arr = arr[y0:y1, x0:x1, :3]
    points = np.zeros((2, 2), dtype=int)
    for i, c in enumerate(((255, 0, 0), (0, 255, 0))):
        points[i] = np.argwhere(np.all(np.equal(arr, c), axis=2))
    return arr_bin[y0:y1, x0:x1], points


if __name__ == '__main__':
    img = Image.open('./res/dragon.png')
    arr, points = crop(np.array(img))
    figure = Figure(arr, points)
    out = Path('./out/')
    out.mkdir(exist_ok=True)
    Image.fromarray(~arr).save(out / 'dragon_0.png')
    for i in range(16):
        arr = figure.next()
        Image.fromarray(~arr).save(out / f'dragon_{i+1}.png')
