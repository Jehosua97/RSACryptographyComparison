import time
import numpy as np
from typing import Callable, List

def measure_times(func:Callable[[int],int], samples:List[int]) -> np.ndarray:
    times=[]
    for m in samples:
        t0=time.perf_counter_ns()
        _=func(m)
        t1=time.perf_counter_ns()
        times.append(t1-t0)
    return np.array(times)
