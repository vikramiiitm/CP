class fastfib:
    def __init__(self):
        self.memo = {}

    def fib(self,n):
        if n < 2:
            return n

        if n in self.memo:
            return self.memo[n]

        else:
            k = self.fib(n-1) + self.fib(n-2)

        self.memo[n] = k

        return k

f = fastfib()

print(f.fib(10))
print(f.memo)