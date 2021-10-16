def merge_sort(arr):
    if len(arr) <= 1:
        return
    mid = len(arr)//2

    left = arr[:mid]
    right = arr[mid:]

    merge_sort(left)
    merge_sort(right)

    merge_list(left,right,arr)
def merge_list(a,b,arr):
    i = j = k = 0
    len_a = len(a)
    len_b = len(b)

    while i<len_a and j < len_b:
        if a[i] <= b[j]:
            arr[k] = a[i]
            i+=1
        else:
            arr[k] = b[j]
            j+=1
        k+=1
    
    while  i < len_a:
        arr[k] = a[i]
        i+=1
        k+=1

    while  j < len_b:
        arr[k] = b[j]
        j+=1
        k+=1

if __name__ == '__main__':
    a=[1,4,2,7,5]
    merge_sort(a)
    print(a)