import secrets
from dataclasses import dataclass
from .math_utils import modinv

@dataclass
class RSAKey:
    n:int; e:int; d:int; p:int; q:int; dp:int; dq:int; qinv:int

# minimal prime generator (educational)
def _random_prime(bits:int)->int:
    import random
    def is_probable_prime(n:int)->bool:
        if n<2: return False
        small=(2,3,5,7,11,13,17,19,23,29)
        if any(n%p==0 for p in small):
            return n in small
        d,s=n-1,0
        while d%2==0:
            d//=2; s+=1
        for a in (2,325,9375,28178,450775,9780504,1795265022):
            if a % n == 0: continue
            x=pow(a,d,n)
            if x in (1,n-1): continue
            for _ in range(s-1):
                x=(x*x)%n
                if x==n-1: break
            else:
                return False
        return True
    while True:
        cand = secrets.randbits(bits) | 1 | (1 << (bits-1))
        if is_probable_prime(cand):
            return cand

def generate_keypair(bits:int=1024,e:int=65537):
    half=bits//2
    while True:
        p=_random_prime(half)
        q=_random_prime(bits-half)
        if p==q: continue
        phi=(p-1)*(q-1)
        import math
        if math.gcd(e,phi)==1:
            break
    d=modinv(e,phi)
    return RSAKey(n=p*q,e=e,d=d,p=p,q=q,dp=d%(p-1),dq=d%(q-1),qinv=modinv(q,p))

def rsa_encrypt(m:int,key:RSAKey)->int:
    return pow(m,key.e,key.n)
