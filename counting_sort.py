def getCountingSorting(arr: list) -> list:
    if not arr:
        return []
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    result = []
    for i in range(len(count)):
        result.extend([i] * count[i])
    return result
