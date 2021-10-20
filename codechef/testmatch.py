#  Test Match Series Problem
# Code: TESTSERIES

def win(list):
    INDIA = list.count(1)
    ENGLAND = list.count(2)

    if INDIA > ENGLAND:
        return "INDIA"
    elif ENGLAND > INDIA:
        return "ENGLAND"
    elif ENGLAND == INDIA:
        return 'DRAW'



testcase = int(input())

winner = {}

for i in range(testcase):
    inputlist = list(map(int,input().split()))
    k = win(inputlist)
    print(k)


