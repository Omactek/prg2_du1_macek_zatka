list = ["b","f","d","z","y","k"]

def preved(array, start, end):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        while low <= high and array[high] >= pivot:
            high = high - 1

        while low <= high and array[low] <= pivot:
            low = low + 1

        if low <= high:
            array[low], array[high] = array[high], array[low]
        else:
            break

    array[start], array[high] = array[high], array[start]

    return high

def quick_sort(array, start, end):
    if start >= end:
        return

    p = preved(array, start, end)
    quick_sort(array, start, p-1)
    quick_sort(array, p+1, end)

quick_sort(list, 0, len(list)-1)
print(list)