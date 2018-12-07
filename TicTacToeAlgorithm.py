import numpy as np

INF = 99999999999999


def evaluate_position(t):
    vd1 = 0
    vd2 = 0

    for x in range(0, 3):
        vr = vc = 0
        for y in range(0, 3):
            if t[x, y] == b'o':
                vr += 1
            elif t[x, y] == b'x':
                vr -= 1

            if t[y, x] == b'o':
                vc += 1
            elif t[y, x] == b'x':
                vc -= 1

        if t[x, x] == b'o':
            vd1 += 1
        if t[x, x] == b'x':
            vd1 -= 1

        if t[x, 2 - x] == b'o':
            vd2 += 1
        if t[x, 2 - x] == b'x':
            vd2 -= 1

        if vr == 3 or vc == 3:
            return 1
        if vr == -3 or vc == -3:
            return -1

    if vd1 == 3 or vd2 == 3:
        return 1

    if vd1 == -3 or vd2 == -3:
        return -1

    return 0


def dfs(ttt, level, move):

    if level == 4:
        return 0

    ev = evaluate_position(ttt)

    if ev == 1:
        if level == 1:
            return INF
        return 1
    elif ev == -1:
        if level == 2:
            return -INF
        return -1

    total = 0
    for a in range(0, 3):
        for b in range(0, 3):
            if ttt[a, b] == b'a':
                ttt[a, b] = move

                total += dfs(ttt, level + 1, b'o' if move == b'x' else b'x')
                ttt[a, b] = b'a'

    return total


tic_tac_toe = np.chararray((3, 3))
tic_tac_toe[:] = 'a'

while True:

    final_q = -1
    print(tic_tac_toe)

    r = int(input())
    c = int(input())

    tic_tac_toe[r, c] = b'x'

    r = -1
    c = -1

    for i in range(0, 3):
        for j in range(0, 3):
            if tic_tac_toe[i, j] == b'a':
                tic_tac_toe[i, j] = b'o'
                q = dfs(tic_tac_toe, 1, b'x')
                if q > final_q:
                    r = i
                    c = j
                    final_q = q

                tic_tac_toe[i, j] = b'a'
    tic_tac_toe[r, c] = b'o'
