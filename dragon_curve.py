import numpy as np

chars = ('  ', '██')

A = np.array((0, 0))
B = np.array((0, 2))

field = np.array(((1, 1, 1),))

rot90 = np.array(((0, -1), (1, 0)))
dst_sign = np.array((-1, 1)).reshape(-1, 1)

dst = np.array((B, np.array(field.shape) - B - 1))

for i in range(8):
    C = rot90 @ (A - B) + B
    dst_roll = np.roll(dst, 1)
    dst_next = np.maximum(dst, dst_roll)

    shift = dst_next - dst
    for D in (A, B, C):
        D += shift[0]

    dst_next += dst_sign @ (B - C).reshape(1, -1)

    field_next = np.zeros(np.sum(dst_next, axis=0) + 1, dtype=int)
    y0, x0 = B - dst[0]
    y1, x1 = B + dst[1] + 1
    field_next[y0:y1, x0:x1] = field
    y0, x0 = B - dst_roll[0]
    y1, x1 = B + dst_roll[1] + 1
    field_next[y0:y1, x0:x1] |= np.rot90(field)

    B = C
    dst = dst_next
    field = field_next


r = '\n'.join(''.join(chars[c] for c in r) for r in field)
print(r)
