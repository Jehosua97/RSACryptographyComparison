from typing import Tuple

def egcd(a:int,b:int)->Tuple[int,int,int]:
    if b==0:
        return (a,1,0)
    g,x1,y1 = egcd(b,a%b)
    return (g,y1,x1-(a//b)*y1)

def modinv(a:int,m:int)->int:
    g,x,_ = egcd(a,m)
    if g!=1:
        raise ValueError('No inverse')
    return x % m

def ct_select(a:int,b:int,sel:int)->int:
    mask = -int(bool(sel))
    return (a & ~mask) | (b & mask)
