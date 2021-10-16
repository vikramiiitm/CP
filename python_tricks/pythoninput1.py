from sys import stdin,stdout
import timeit

def sum():
    start = timeit.default_timer()
    arr = [1,2,3,4,5,6,7,8,9,11,12,13,15,16,12,121,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,23,34,4,5,5,6,7,7,8,8,9,6,5,4,2,4,5,6,6,8,9]
    print("arr : ",arr)
    end = timeit.default_timer()
    print("exec : ",end-start)

def sum2():
    start = timeit.default_timer()
    arr = [1,2,3,4,5,6,7,8,9,11,12,13,15,16,12,121,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,23,34,4,5,5,6,7,7,8,8,9,6,5,4,2,4,5,6,6,8,9]
    stdout.write("arr : " + str(arr))
    end = timeit.default_timer()
    stdout.write("exec : " + str(end-start))
    
    
sum()
sum2()