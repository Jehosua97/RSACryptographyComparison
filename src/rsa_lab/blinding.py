import secrets
from .math_utils import modinv
from .rsa_primitives import RSAKey

def blind_message(m:int,key:RSAKey):
    n,e = key.n, key.e
    while True:
        r = secrets.randbelow(n-2)+2
        if r%key.p!=0 and r%key.q!=0:
            break
    r_e = pow(r,e,n)
    return (m*r_e)%n, r

def unblind(c:int,r:int,key:RSAKey)->int:
    rinv = modinv(r,key.n)
    return (c*rinv)%key.n

def exponent_blind(d:int,phi:int)->int:
    k = secrets.randbits(64)
    return d + k*phi
