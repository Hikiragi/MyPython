def heap(arr: list, lenght: int, item: int) -> list:
    largest = item
    left = 2 * item + 1
    right = 2 * item + 2
    if left < lenght and arr[item] < arr[left]:
        largest = left
    if right < lenght and arr[largest] < arr[right]:
        largest = right
    if largest != item:
        arr[item], arr[largest] = arr[largest], arr[item]
        heap(arr, lenght, largest)


def getHeapifySorting(arr: list) -> list:
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heap(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heap(arr, i, 0)
    return arr