import random
from sympy import isprime
from decimal import Decimal
from fractions import Fraction
from itertools import combinations
import math

# Вывод матрицы в терминал
def print_matrix(matrix):
    for row in matrix:
        print(*row)
    print()

# Нод двух чисел
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#Цепная дробь
def sqrt_to_chain_(a, k=20):
    sq = Decimal(a).sqrt()
    res = [int(sq)]
    while k != 0:
        fractional_part = sq - int(sq)
        if fractional_part == 0:
            break
        sq = 1 / Fraction(fractional_part)
        res.append(int(sq))
        sq -= int(sq)
        k -= 1
    return res

# Вычисление подходящих дробей
def suitable_fractions_chain(chain, k=20):
    P = [0, 1] 
    Q = [1, 0]
    for i in range(len(chain)):
        q = chain[i]
        P.append(q * P[-1] + P[-2])
        Q.append(q * Q[-1] + Q[-2])
    return P[2:], Q[2:]

# Алгоритм ро-полларда
def pollard_ro(n, eps):
    if n == 1:
        return 1
    k = int(math.sqrt(2*math.sqrt(n)*math.log(1 / eps))) + 1 
    divs = set()
    for i in range(k):
        x = random.randint(1, n - 1)
        y, i, stage = 1, 0, 2
        while gcd(n, abs(x - y)) == 1:
            if i == stage:
                y = x
                stage = stage * 2
            x = (x * x + 1) % n
            i += 1
        divs.add(gcd(n, abs(x - y)))
    return sorted(list(divs))

# Алгоритм р - 1 полларда
def pollard_p(n, B=1000, k=100):
    res = set()
    for _ in range(k):
        a = random.randint(2, n - 2)
        d = gcd(a, n)
        if d > 1:
            res.add(d)
        for i in range(2, B):
            a = pow(a, i, n)
            d = gcd(a - 1, n)
            if 1 < d < n:
                res.add(d)
    return sorted(list(res))

# Вычисление символа якоби
def jacobi(a, n):
    a = a % n
    t = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n
    return t if n == 1 else 0

# Генерирование факторной базы
def gen_base(num=512, len_=5):
    B = [-1]
    for i in range(2, num):
        if isprime(i) and jacobi(num, i) == 1:
            B.append(i)
        if len(B) == len_:
            return B
    return B

# Разложение числа по факторной базе
def get_factor_base(base, num, m):
    res = []
    res_pows = []
    if num < 0:
        res.append(1)
        res_pows.append((-1, 1))
    else:
        res.append(0)
        res_pows.append((-1, 0))
    num = abs(num)
    for p in base[1:]:
        count = 0
        while num % p == 0:
            num //= p
            count += 1
        res.append(count % 2)
        res_pows.append((p, count))
    while len(res) != len(base):
        res.append(0)
    if num != 1:
        return None, None
    return res, res_pows

# Вычисление модуля в поле
def abs_(p, n, q):
    return pow(p, 2) - n * pow(q, 2)

# XOR двоичных векторов
def xor_vectors(vectors):
    result = [0] * len(vectors[0])
    for vector in vectors:
        result = [result[i] ^ vector[i] for i in range(len(result))] 
    return result

# Поиск единичного вектора путем комбинации
def find_zero_vector_combination(matrix):
    zero_vector = [0] * len(matrix[0])
    results = []
    for r in range(2, len(matrix) + 1):
        for combo in combinations(range(len(matrix)), r):
            selected_vectors = [matrix[i] for i in combo]
            if xor_vectors(selected_vectors) == zero_vector: 
                results.append(combo)
    return results

# Сумма по комбинациям
def find_sum(comb, pows, i):
    sum_ = 0
    for index in comb:
        sum_ += pows[index][i][1]
    return sum_ // 2

# Метод цепных дробей
def CFRAC(n, len_base=20):
    chain = sqrt_to_chain_(n, len_base)
    P, Q = suitable_fractions_chain(chain, len_base)
    base = gen_base(n, len_base)
    h = len(base)
    system = []
    P_k = [] # Числа которые подошли 
    pows_ = [] # Для найденных числе запишем показатели чисел
    for i, p in enumerate(P):
        if len(system) != h + 2:
            min_sub = abs_(p, n, Q[i])
            factor, pows = get_factor_base(base,  min_sub, n)
            if factor != None:
                system.append(factor)
                P_k.append(p)
                pows_.append(pows)
        else:
            break
    combinations = find_zero_vector_combination(system)
    for comb in combinations:
        x = 1
        for i in comb:
            x *= P_k[i]
        x %= n
        y = 1
        i = 1
        for p in enumerate(base[1:]):
            sum_ = find_sum(comb, pows_, i)
            y *= pow(base[i], sum_)
            i += 1
        y %= n
        p = 1
        # print(x, y)
        if x % n != y % n and x % n != -y % n:
            return gcd(x - y, n)
    return CFRAC(n, len_base + 10)

# Проверка на полную степень
def is_perfect_power(n):
    if n < 2:
        return False

    # Проверяем для всех возможных степеней k, начиная с 2
    for k in range(2, int(math.log(n, 2)) + 1):
        x = int(round(n ** (1 / k)))
        if x ** k == n:
            return True, x, k

    return False, None, None

if __name__ == "__main__":
    type_ = """Введите тип факторизации: \n
1 - ρ-метод Полларда
2 - (p-1)-метод Полларда
3 - Метод цепных дробей 
4 - Использовать сразу все методы
5 - Выход\n"""
    print(type_)
    param = None
    while param not in ["1", "2", "3", "4", "5"]:
        param = input(":>")
        match param:
            case "1":
                print("Выбран ρ-метод Полларда")
                a = input("Введите число а для разложения: ")
                k = input("Укажите e (0 < e < 1): ")
                lst_factors = pollard_ro(int(a), float(k))
                print(f"Делители числа {a}: ", lst_factors)
                print("Проверка:")
                for i, num in enumerate(lst_factors):
                    print(f"{i + 1}) {int(a) / num} * {num} = {int(a) / num * num}")
                param = None
            case "2":
                print("Выбран (p-1)-метод Полларда")
                a = input("Введите число а для разложения: ")
                k = input("Укажите B для построения базы: ")
                lst_factors = pollard_p(int(a), int(k))
                print(f"Делители числа {a}: ", lst_factors)
                for i, num in enumerate(lst_factors):
                    print(f"{i + 1}) {int(a) / num} * {num} = {int(a) / num * num}")
                param = None
            case "3":
                print("Выбран Метод цепных дробей")
                a = input("Введите число а для разложения: ")
                if isprime(int(a)):
                    print("Число является простым!")
                    print(f"Результат: {a}")
                elif Decimal(int(a)).sqrt() ** 2 == a:
                    print(f"{a} квадрат числа {int(Decimal(int(a)).sqrt())}")
                elif is_perfect_power(int(a))[0]:
                    print(f"Делитель: {is_perfect_power(int(a))[1]}")
                elif int(a) % 2 == 0:
                    print(f"Делитель: {int(a) // 2}")
                else:
                    res = CFRAC(int(a))
                    print(f"Делитель: {res}")
                    print(f"Проверка {int(a) / res} * {res} = {int(a) / res * res}")
                param = None
            case "4":
                print("Выбраны сразу все методы")
                a = input("Введите число а для разложения: ")
                k = input("Укажите e (0 < e < 1): ")
                res1 = pollard_ro(int(a), float(k))
                print(f"Делители числа {a}: ", res1)
                print("Проверка для ρ-метода Полларда")
                for i, num in enumerate(res1):
                    print(f"{i + 1}) {int(a) / num} * {num} = {int(a) / num * num}")
                res2 = pollard_p(int(a))
                print(f"Делители числа {a}: ", res2)
                print("Проверка для (p-1)-метода Полларда")
                for i, num in enumerate(res2):
                    print(f"{i + 1}) {int(a) / num} * {num} = {int(a) / num * num}")
                print("Проверка метода цепных дробей")
                if isprime(int(a)):
                    print("Число является простым!")
                    print(f"Результат: {a}")
                elif Decimal(int(a)).sqrt() ** 2 == a:
                    print(f"{a} квадрат числа {int(Decimal(int(a)).sqrt())}")
                elif is_perfect_power(int(a))[0]:
                    print(f"Делитель: {is_perfect_power(int(a))[1]}")
                elif int(a) % 2 == 0:
                    print(f"Делитель: {int(a) // 2}")
                else:
                    res3 = CFRAC(int(a), int(k))
                    print(f"Проверка {int(a) / res3} * {res3} = {int(a) / res3 * res3}")
                param = None
            case "5":
                param = "5"


    def func1(x, m):
        return (x**2 + 1) % m

    a = 1359331
    a = 1373503
    a = 8051
    a = 1728239
    
    # print(pollard_ro(a))
    # a = 8
    # print(pollard_ro(432, 467, func1))
    a = 1557697
    
    # print(pollard_p(a))
    # print(chains(a))
    # chain = sqrt_to_chain_(1081, k=20)

    # print(suitable_fractions_chain(chain, k=20))
    a = 21299881
    a = 16
    a = 7878920942
    # if isprime(a):
    #     print(a)
    # if Decimal(a).sqrt() ** 2 == a:
    #     print(int(a ** 0.5)) 
    # else:
    # res = CFRAC(a, 20)
    # print(res, a / res)
    # a = 27
    # ch =sqrt_to_chain_(a,int(Decimal(a).sqrt()) + 1)
    # print(ch)
    # print(suitable_fractions_chain(ch, int(Decimal(a).sqrt()) + 1))