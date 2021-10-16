import sys
# 1. single line input integers ex. 1 2 3 4
# reference them in separate variable
# a = 1
# b = 2
# c = 3
# d = 4
def get_inps():
    return map(int,sys.stdin.readline().strip().split())
a,b,c,d = get_inps()

# 2. single line input integers ex. 1 2 3 4
# to single variable we convert theoutput of map to list
# ex. a = [1,2,3,4,5]
def get_list():
    return list(map(int,sys.stdin.readline().strip().split()))

# 3. Take input of strings ex. arr = Geeks is the best

def get_string():
    return sys.stdin.readline().strip()

