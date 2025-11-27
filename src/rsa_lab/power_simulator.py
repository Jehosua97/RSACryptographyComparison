import numpy as np

def hamming_weight(x:int)->int:
    return x.bit_count()

def simulate_trace_square_multiply(m:int,d:int,n:int,noise_std:float=1.0):
    rng = np.random.default_rng()
    r=1
    x=m%n
    trace=[]
    for bit in bin(d)[2:]:
        r=(r*r)%n
        trace.append(hamming_weight(r)+rng.normal(0,noise_std))
        if bit=='1':
            r=(r*x)%n
            trace.append(hamming_weight(r)+rng.normal(0,noise_std))
    return np.array(trace)

def simulate_trace_always(m:int,d:int,n:int,noise_std:float=1.0):
    rng = np.random.default_rng()
    r=1
    x=m%n
    trace=[]
    for _ in bin(d)[2:]:
        r_sq=(r*r)%n
        trace.append(hamming_weight(r_sq)+rng.normal(0,noise_std))
        r_mul=(r_sq*x)%n
        trace.append(hamming_weight(r_mul)+rng.normal(0,noise_std))
        r=r_mul
    return np.array(trace)
