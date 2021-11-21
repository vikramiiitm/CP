def ArrayChallenge(arr):
  num = arr[0]
  lis = arr[1:]
  r = len(lis)-num
  median = []
  print("r",r)
  for i in range(r+1):
    print(i)
    for j in lis[i:i+r]:
      print(j)

Arra=[5,2,4,6]

ArrayChallenge(Arra)