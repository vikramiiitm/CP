def PrintNto1(n):
    #base comndtion
    if n==1:             
        print(n)
        return
    print(n) #inducton
    #hypothis for smaller input
    PrintNto1(n-1)           
# Print1toN(15)s
PrintNto1(4)