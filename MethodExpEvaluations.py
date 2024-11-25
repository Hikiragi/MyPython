import numpy as np
from collections import Counter


def find_expert_assessment(indexCol):
    col = startArr[:, indexCol]
    comparison_matrix = np.zeros((len(col), len(col)), dtype=int)
    for i in range(len(col)):
        for j in range(len(col)):
            # print(f"col[i]: {col[i]}\nCol[j]: {col[j]}\n")
            comparison_matrix[i, j] = col[i] <= col[j]
    return comparison_matrix


def find_ratio_exp(matrix):
    ratioExpArr = []
    res = 1
    for i in range(len(matrix)):
        for j in matrix[i]:
            res *= j
        ratioExpArr.append(res ** (1 / len(matrix[i])))
        res = 1
    return ratioExpArr


def find_ranging(matrix):
    print(f"Построение матриц ранжировок экспертов: ")
    for item in range(len(matrix.T)):
        print(f"Y{item + 1}: \n{find_expert_assessment(item)}\n")
    name = {}
    for item in range(len(matrix.T)):
        name[f"Y_{item + 1}"] = find_expert_assessment(item)
    all_Y = 0
    for item in name.values():
        all_Y += item
    all_ranging = []
    for item in range(len(all_Y)):
        for j in all_Y[item]:
            if j >= len(all_Y[item]) / 2:
                all_ranging.append(1)
            else:
                all_ranging.append(0)
    all_ranging = np.array(all_ranging).reshape(-1, 5)
    return all_ranging


def calculate_counters(matrix):
    counters = {}
    schet = 0
    for item in matrix.T:
        counters[f"Hj_{schet + 1}"] = Counter(item)
        schet += 1
    return counters


def calculate_Hj(counters, matrix):
    Hj = {}
    for key, vals in counters.items():
        if len(vals.values()) == len(matrix.T[0]):
            Hj[key] = int(False)
        else:
            Hj[key] = int(True)
    return Hj


def calculate_hk(counters):
    hk = {}
    schet = 0
    for keys, vals in counters.items():
        hk[f"hk_{schet + 1}"] = []
        for key, val in vals.items():
            if val > 1:
                hk[f"hk_{schet + 1}"].append(val)
        schet += 1
    for key, value in hk.items():
        hk[key] = sum(value)
    return hk


def calculate_Tj(hk):
    Tj = {}
    schet = 0
    for key, value in hk.items():
        Tj[f"Tj_{schet + 1}"] = (value ** 3) - value
        schet += 1
    return Tj


startArr = np.array([
    [5, 1, 2, 4],
    [4, 2.5, 3, 2],
    [3, 4.7, 4, 3],
    [2, 2.5, 1.2, 4],
    [1, 2.5, 2.5, 2]
])

# startArr = np.array([
#     [2, 3, 2.8, 5],
#     [3, 1.5, 5, 4.7],
#     [3, 3.7, 3.2, 1.7],
#     [1, 2, 3.2, 4.7],
#     [1, 2, 2, 2.8]
# ])

matrix_b = np.dot(startArr, startArr.T)
matrix_c = np.dot(startArr.T, startArr)
vector_b, v = np.linalg.eig(matrix_b)
vector_c, v1 = np.linalg.eig(matrix_c)
print(f"Начальная матрица: \n{startArr}\n")
print(f"Матрица B: \n{matrix_b}")
print(f"Ветор матрицы B: \n{[item for item in vector_b]}\n")
print(f"Коэффициент обобщенной оценки объектов матрицы B: \n{find_ratio_exp(matrix_b)}\n")
print(f"Матрица С: \n{matrix_c}")
print(f"Вектор матрицы C: \n{[item for item in vector_c]}\n")
print(f"Коэффициент обощенной оценки объекто матрицы C: \n{find_ratio_exp(matrix_c)}\n")
ranging = find_ranging(startArr)
print(f"Обобщенная ранжировка: \n{ranging}")

counters = calculate_counters(startArr)
Hj = calculate_Hj(counters, startArr)
hk = calculate_hk(counters)
Tj = calculate_Tj(hk)
# Расчет Ri
Ri = []
for item in startArr:
    Ri.append(sum(item))

# Расчет среднего R
Rmid = sum(Ri) / len(Ri)

# Расчет (Ri - Rmid)^2
RiMidQvadro = []
for item in Ri:
    RiMidQvadro.append((item - Rmid) ** 2)

# Расчет S
S = sum(RiMidQvadro)

# Расчет W
W = (12 * S) / (((startArr.shape[1] ** 2) * ((startArr.shape[0] ** 3) - startArr.shape[0])) - startArr.shape[1] * sum(
    Tj.values()))
# Вывод результатов
for key, value in Hj.items():
    print(f"{key}: {value}", end=" ")
print()

for key, value in hk.items():
    print(f"{key}: {value}", end=" ")
print()

for key, value in Tj.items():
    print(f"{key}: {value}", end=" ")
print()

for item in Ri:
    print(f"Ri: {item}")

print(f"R среднее: {round(Rmid, 4)}")

for item in RiMidQvadro:
    print(f"Квадрат Ri - R среднее: {round(item, 4)}")

print(f"S: {round(S, 4)}")

print(f"W: {round(W, 4)}")
