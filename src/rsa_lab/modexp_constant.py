def modexp_always(m:int,d:int,n:int)->int:
    r=1
    x=m%n
    for bit in bin(d)[2:]:
        r_sq=(r*r)%n
        r_mul=(r_sq*x)%n
        is_one=1 if bit=='1' else 0
        r=(r_mul*is_one + r_sq*(1-is_one))%n
    return r

def modexp_ladder(m:int,d:int,n:int)->int:
    r0, r1 = 1, m%n
    for bit in bin(d)[2:]:
        if bit=='0':
            r1=(r0*r1)%n
            r0=(r0*r0)%n
        else:
            r0=(r0*r1)%n
            r1=(r1*r1)%n
    return r0
