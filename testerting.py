def ct2(s):
    res = ""
    n = 0
    for c in s:
        if c.isalpha():
            res += c.upper()
            n += (ord(c) - ord('b'))
        elif c.isalnum():
            res = "!" + res[:-1]
            print(res, n)
        else:
            s = str(n-1)
            res = res.replace("!", s)
            n = 3
    return res
print(ct2("3*b 2c"))