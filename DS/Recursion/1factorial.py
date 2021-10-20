def fact(n):
    # base
    if n == 1:
        return n

    # hypo on small input
    else:
        return n*fact(n-1)

k = fact(5)
print(k)