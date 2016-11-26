from math import cos
from datetime import datetime
from multiprocessing.pool import Pool


def timeit(foo):
    b = datetime.now()
    res = foo()
    e = datetime.now()
    return res, e-b


if __name__ == "__main__":
    pool = Pool(32)
    data = [i for i in range(0, 10**8)]
    print(timeit(lambda : list(pool.map(cos, data)))[1])
    print(timeit(lambda : list(map(cos, data)))[1])
