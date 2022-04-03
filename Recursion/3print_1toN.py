def Print1toN(n):
    #base comndtion
    if n==1:             
        print(1)
        return
    #hypothis for smaller input
    Print1toN(n-1)           

    print(n) #inducton

    