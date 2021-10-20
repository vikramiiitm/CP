# Problem Code: LUCKYNUM
"""
Chef buys a lottery ticket that has a 3 
digit code associated with it. He thinks 
that digit 7 is his lucky digit and brings 
him good luck. Chef will win some amount in the 
lottery if at least one of the digits of the lottery ticket is 7
Given three digits A
, B, and C of the lottery ticket, tell whether Chef
wins something or not?
"""

def win(list):
    seven = 7
    if 7 in list:
        return 'Yes'
    else:
        return 'NO'
testcase = int(input())

for i in range(testcase):
    inputlist = list(map(int,input().split()))
    output = win(inputlist)
    print(output)
