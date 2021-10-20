#  Maximum Number Of Distinct Elements 
# Problem Code: MAXDISTKT

def distinctelement(B,n):
    possible = {}

    for i in B:
        possible[i] = i-1

    for key,val in possible.items():
        



testcase = int(input())
for i in range(testcase):
    n = int(input())
    B = list(map(int, input().split()))

    distinctcase(B,n)

    






