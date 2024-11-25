
def binary_search(mas, item):
    low = 0
    high = len(mas) - 1

    while low <= high:
        mid = int((low + high) / 2)
        guess = sorted(mas)[mid]
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None

my_lst = [12, 1, 2, 3, 5, 7, 8, 9, 10, 14, 18, 19]
print(binary_search(my_lst, 9))