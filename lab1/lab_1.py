from math import log2, gcd
from copy import deepcopy
import itertools
import interface as interface

# Обычный алгоритм Евклида (НОД двух чисел) 
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Бинарный алгоритм Евклида 
def gcd_bin(a, b):
    if a < b:
        a, b = b, a
    while b != 0:
        e = int(log2(a / b))
        t = min(pow(2, e + 1) * b - a, a - pow(2, e) * b)
        if t <= b:
            a, b = b, t
        else:
            a, b = t, b
    return a

# Расширенный алгоритм Евклида
def gcd_xt(a, b):
    s0, t0 = 1, 0
    s1, t1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return s0, t0, a

# Нахождение произведения элеметов в массиве
def prod(list):
    res = 1
    for val in list: res *= val
    return res

# Китайсткая теорема об остатках (система сравнений)
def china_theorem(params, moduls):
    M = prod(moduls)
    u = 0
    for i, m in enumerate(moduls):
        c = M // m 
        d, _, _ = gcd_xt(c, m)
        u += c * d * params[i]
    return u % M

# Алгоритм Гарнера (система сравнений)
def garner_alg(params, moduls):
    k = len(moduls)
    u, q = 0, [0] * k
    for i in range(k):
        q[i] = params[i]
        for j in range(i):
            if i != j:
                d, _, _ = gcd_xt(moduls[j], moduls[i])
                q[i] = ((q[i] - q[j]) * d) % moduls[i]
    factor = 1
    for i in range(k):
        u += q[i] * factor
        factor *= moduls[i]
    return u % prod(moduls)

# Вывод матрицы в терминал
def print_matrix(matrix):
    for row in matrix:
        print(*row)
    print()

# Получение матрицы коэфициентов системы и вектора свободных членов
def get_matrix_A_and_vector(system):
    A, vec = [], []
    for row in system:
        A.append(row[:-1])
        vec.append(row[-1])
    return A, vec

# Умножение строки матрицы на число в кольце по модулю p
def mul_row_on_num(vec, num, p):
    return list(map(lambda x: x * num % p, vec))

# Сложение строк матрицы по модулю p
def add_rows_mod(row1, row2, p):
    res = []
    for i in range(len(row1)):
        res.append((row1[i] + row2[i]) % p)
    return res

# Получение новой матрицы B из матрицы коэфициаентов А,
# вектора свобоных членов и единичной матрицы
def get_matrix_B(A, vec, p):
    B, n, m = [], len(A[0]), len(A)
    vec = mul_row_on_num(vec, -1, p)
    for i in range(m):
        new_row = A[i] + [vec[i]]
        B.append(new_row)
    for i in range(n):
        buff = []
        for j in range(n + 1):
            if i == j:
                buff.append(1)
            else:
                buff.append(0)
        B.append(buff)
    return B

# Перестановка строк в матрице
def swap_row(matrix, row1, row2):
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]

# Перестановка столбцов в матрице
def swap_col(matrix, index1, index2):
    for row in matrix:
        row[index1], row[index2] = row[index2], row[index1]

# Вычитание столбцов по модулю 
def sub_colums(matrix, index1, index2, factor, m):
    for row in matrix:
        row[index1] -= factor * row[index2]
        row[index1] %= m

# Сложение столбцов по модулю 
def add_columns_mod(matrix, col1, col2, m):
    num_rows = len(matrix) 
    for i in range(num_rows):
        matrix[i][col1] = (matrix[i][col1] + matrix[i][col2]) % m

# Умножение столбца на число по модулю
def mul_column_on_num(matrix, col, multiplier, m):
    num_rows = len(matrix) 
    for i in range(num_rows):
        matrix[i][col] = (matrix[i][col] * multiplier) % m

# Поиск ненулевого элемента в столбце начиная со строки start
def find_not_zero_elem_in_col(matrix, start, end, col):
    for i in range(start, end):
        if matrix[i][col] != 0:
            return i
    return None

# Преобразование столбца в строку
def col_to_vec(matrix, col, row):
    res = []
    for i in range(row, len(matrix)):
        res.append(matrix[i][col])
    return res

# Приведение матрицы к верхней треугольной
def triangular_matrix(matrix, m, n, p):

    for k in range(min(n , m)):
        if matrix[k][k] == 0:
            i_new_row = find_not_zero_elem_in_col(matrix, k, m, k)
            if i_new_row is not None:
                swap_row(matrix, k, i_new_row)

        min_el = float('inf')
        min_index = None

        for j in range(k, n):
            if matrix[k][j] != 0 and abs(matrix[k][j]) < abs(min_el):
                min_el = matrix[k][j]
                min_index = j

        if min_index is not None and k != min_index:
            swap_col(matrix, k, min_index)
        
        inv, _, _ = gcd_xt(matrix[k][k], p)
        inv %= p

        for j in range(k + 1, n):
            if matrix[k][j] != 0 and j != k:
                factor = (matrix[k][j] * inv) % p
                sub_colums(matrix, j, k, factor, p)
    return matrix

# Поиск корней системы уравнений в кольце целых чисел
def find_roots(matrix, p, n, m):

    # Обнуляем свободные члены
    for k in range(min(m, n)):
        inv, _, _ = gcd_xt(matrix[k][k], p)
        inv %= p
        factor = (matrix[k][-1] * inv) % p
        sub_colums(matrix, n, k, factor, p)
    for i in range(m):
        if matrix[i][-1] != 0:
            return "Не имеет решения в целых числах"
    roots = []
    
    # Получаем линейную комбинацию 
    for comb in itertools.product(range(p), repeat=(n - min(m, n))):
        start_i = -1
        f = col_to_vec(matrix, start_i, m)
        for i in range(n - min(m, n)):
            start_i -= 1
            new_row = col_to_vec(matrix, start_i, m)
            f = add_rows_mod(f, mul_row_on_num(new_row, comb[i], p), p)
        roots.append(f)
    
    print_matrix(matrix)

    return roots

# Функция Гаусса решения системы уравнений в кольце    
def gauss_mod(system, p):
    A, vec = get_matrix_A_and_vector(system)
    B = get_matrix_B(A, vec, p)
    m, n = len(A), len(A[0])
    triangular = triangular_matrix(B, m, n, p)
    print_matrix(triangular)
    return find_roots(triangular, p, n, m)


if __name__ == "__main__":
    print(interface.start_massage)
    param = None
    while param not in ["1", "2", "3", "4", "5", "6"]:
        param = input(":>").strip()
        match param:
            case "1":
                print("Алгоритм Евклида нахождения НОД двух чисел")
                print("Укажите два числа a и b: \n")
                a = input("a = ")
                b = input("b = ")
                print(f"gcd(a, b) = {gcd(int(a), int(b))} \n")
                param = None
            case "2": 
                print("Бинарный алгоритм Евклида нахождения НОД двух чисел")
                print("Укажите два числа a и b: \n")
                a = input("a = ")
                b = input("b = ")
                print(f"gcd(a, b) = {gcd_bin(int(a), int(b))}")
                param = None
            case "3": 
                print("Расширенный алгоритм Евклида")
                print("Укажите два числа a и b: \n")
                a = input("a = ")
                b = input("b = ")
                print(f"Надем такие коэфициенты x и y что: x{a} + y{b} = gcd({a}, {b})")
                x, y, gcd_ = gcd_xt(int(a), int(b))
                print(f"Выход: x = {x}, y = {y}, gcd = {gcd_}")
                print("Проверка:")
                if y < 0:
                    print(f"{x}*{a} - {abs(y)}*{b} = {gcd_}")
                else:
                    print(f"{x}*{a} + {y}*{b} = {gcd_}")
                param = None
            case "4": 
                print("Решение системы сравнений первой степени (Китайская теорема об остатках)")
                flag = False 
                while not flag:
                    u = input("Укажите множество параметров U через пробел: \n").split()
                    m = input("Укажите множество взаимопростых параметров m через пробел: \n").split()
                    if interface.check_params(u, m):
                        flag = True
                    else:
                        print("Введены некорректные данные!!!")
                        flag = False
                u = list(map(lambda x: int(x), u))
                m = list(map(lambda x: int(x), m))
                print("В результате имеем систему сравнений следующего вида:")
                for i in range(len(u)):
                    print(f"u ≡ {u[i]} (mod {m[i]})")
                res = china_theorem(u, m)
                print(f"Ответ: u = {res}")
                print("Осуществим проверку")
                for i in range(len(u)):
                    print(f"{res % m[i]} == {u[i] % m[i]}")
                param = None
            case "5": 
                print("Решение системы сравнений первой степени (Алгоримт Гарнера)")
                flag = False 
                while not flag:
                    u = input("Укажите множество параметров U через пробел: \n").split()
                    m = input("Укажите множество взаимопростых параметров m через пробел: \n").split()
                    if interface.check_params(u, m):
                        flag = True
                    else:
                        print("Введены некорректные данные!!!")
                        flag = False
                u = list(map(lambda x: int(x), u))
                m = list(map(lambda x: int(x), m))
                print("В результате имеем систему сравнений следующего вида:")
                for i in range(len(u)):
                    print(f"u ≡ {u[i]} (mod {m[i]})")
                res = garner_alg(u, m)
                print(f"Ответ: u = {res}")
                print("Осуществим проверку")
                for i in range(len(u)):
                    print(f"{res % m[i]} == {u[i] % m[i]}")
                param = None
            case "6": 
                print("Решение системы уравнений первой степени в кольце целых чисел (Алгоримт Гаусса)")
                file = input("Укажите файл с записанной системой и модулем: ")
                data = interface.parse_file(file)
                for i, pair in enumerate(data):
                    m = pair[0]
                    system = pair[1]
                    cop_system = deepcopy(system) 
                    print(f"Система {i + 1} (Модуль {m}): \n")
                    print_matrix(system)
                    roots = gauss_mod(system, m)
                    roots.sort()
                    print(f"Вектор свободных членов: \n")
                    vec = []
                    for i in range(len(system)):
                        vec.append(system[i][-1])
                    print(vec, "\n")
                    x_i = " ".join([f"x{i + 1}" for i in range(len(system[0]) - 1)])
                    print(f"Полное решение: \n")
                    print(x_i)
                    print_matrix(roots)
                    print(f"Осуществим проверку")
                    for root in roots:
                        res = []
                        for j in range(len(cop_system)):
                            sum_ = 0
                            for i in range(len(cop_system[j]) - 1):
                                sum_ += cop_system[j][i] * root[i]
                            res.append(sum_ % m) 
                        print(f"Для решения {root} получен след вектор свободных членов: {res}")
                param = None