def modexp_vuln(m:int,d:int,n:int)->int:
    result=1
    base=m%n
    for bit in bin(d)[2:]:
        result=(result*result)%n
        if bit=='1':
            result=(result*base)%n
    return result
