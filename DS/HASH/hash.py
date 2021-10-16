# stock_prices = []

# with open("/home/vk/Desktop/CP/stock.csv",'r') as f:
#     for line in f:
#         tokens = line.split(',')
#         day = tokens[0]
#         price = float(tokens[1])
#         stock_prices.append([day,price])

# this method is slow imagine if stockhas million entries
# complexity 0(n)
# [print(v[1]) for v in stock_prices if v[0] == "9-Mar"]


# so we will use Dictionary, 0(1)
# stock_prices = {}
# with open("/home/vk/Desktop/CP/stock.csv",'r') as f:
#     for line in f:
#         tokens = line.split(',')
#         day = tokens[0]
#         price = float(tokens[1])
#         stock_prices[day] = price

# [print(k,v,end='\n') for k,v in stock_prices.items()]

# try:
#     k = stock_prices['9-ar']
#     print(k)
# except :
#     print('not exists')


# hash
stock_prices = {}
# with open("/home/vk/Desktop/CP/stock.csv",'r') as f:




class HashTable:
    def __init__(self):
        # making arr of lenth 100
        self.MAX = 100
        self.arr = [None]*self.MAX

    def get_hash(self,key):
        s = 0
        for c in key:
            s += ord(c)
        return s % self.MAX

    def __setitem__(self,key,val):
        h = self.get_hash(key)
        self.arr[h] = val
        print('set item called')

    def __getitem__(self,key):
        h = self.get_hash(key)
        return self.arr[h]
    
    def __delitem__(self,key):
        h = self.get_hash(key)
        self.arr[h] = None


h = HashTable()

h['9-Mar'] = 3022
h['10-Mar'] = 3021
h['11-Mar'] = 3025
h['12-Mar'] = 3026

print(h['9-Mar'])