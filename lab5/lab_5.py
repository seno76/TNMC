import math
import random
from sympy import isprime

# Функция gcd для вычисления наибольшего общего делителя
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Расширенный алгоритм Евклида для нахождения решения сравнений
def gcd_xt(a, b):
    s0, t0 = 1, 0
    s1, t1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return a, s0, t0

# Алгоритм Гельфонда - Шанкса
def log_gelfond_shanks(g, h, m):
    r = int(math.sqrt(m)) + 1
    table = {pow(g, a, m): a for a in range(r)}
    factor = pow(g, -r, m)
    res = []
    for b in range(r):
        value = (h * pow(factor, b, m)) % m
        if value in table:
            res.append(b * r + table[value])
    return min(res)

# Функция f для шага Полларда
def f(a, h, g, p):
    if 0 < a < p / 3:
        return (h * a) % p
    elif p / 3 <= a < 2 * p / 3:
        return pow(a, 2, p)
    else:
        return (g * a) % p

# Функция для обновления a
def set_element_a(y, m, a):
    if 0 < y < m / 3:
        return a % m
    elif m / 3 <= y < 2 * m / 3:
        return (2 * a) % m
    else:
        return (a + 1) % m 

# Функция для обновления b
def set_element_b(y, m, b):
    if 0 < y < m / 3:
        return (b + 1) % m
    elif m / 3 <= y < 2 * m / 3:
        return (2 * b) % m
    else:
        return b % m

# Функция обновления элементов для y, a и b
def set_next_elements(y, a, b, h, g, m):
    new_y = f(y, h, g, m)
    new_a = set_element_a(y, m, a)
    new_b = set_element_b(y, m, b)
    return new_y, new_a, new_b

# Функция решения сравнения
def solve_comparison(a, b, p):
    g = gcd(a, p)
    if g > 1:
        if b % g != 0:
            return []
        a_prime = a // g
        b_prime = b // g
        p_prime = p // g
        _, x_prime, _ = gcd_xt(a_prime, p_prime)
        x_prime = (x_prime * b_prime) % p_prime
        solutions = [(x_prime + k * p_prime) % p for k in range(g)]
        return solutions
    else:
        _, a_inv, _ = gcd_xt(a, p)
        x = (a_inv * b) % p
        return [x]

# Основная функция для расчета дискретного логарифма
def pollard_rho_discrete_log(g, h, m, eps=0.9):
    T = int(math.sqrt(2 * m * math.log(1 / eps))) + 1


    while True:
        i = 1
        s = random.randint(1, m - 1)
        
        y, a, b = set_next_elements(pow(g, s, m), s, 0, h, g, m)
        y1, a1, b1 = set_next_elements(y, a, b, h, g, m)
        count = 10_000
        while True:
            if y == y1:
                d = gcd((b - b1) % m, m)
                lst = solve_comparison((a1 - a) % m, (b - b1) % m, m)

                if not lst:
                    break
                

                for x in lst:
                    if pow(g, x, m) == h % m:
                        return x
            # if i >= T:
            #     return -1 
            if count == 0:
                return -1
            count -= 1 
            i += 1
            y, a, b = set_next_elements(y, a, b, h, g, m)
            y1, a1, b1 = set_next_elements(y1, a1, b1, h, g, m)
            y1, a1, b1 = set_next_elements(y1, a1, b1, h, g, m)

# Является ли заданное число m степенью простого числа
def is_prime_power(m):
    for p in range(2, int(math.sqrt(m)) + 1):
        if isprime(p):
            n = 1
            while p ** n <= m:
                if p ** n == m:
                    return True, p, n
                n += 1
    return False, None, None

# Разложение числа на его простые множители
def find_coprime_factors(m):
    for m1 in range(2, m // 2 + 1):
        if m % m1 == 0:
            m2 = m // m1
            if math.gcd(m1, m2) == 1:
                return True, m1, m2
    return False, None, None

# Проверка на то как раскладывается число m
def check_m_factorization(m):
    prime_power, p, n = is_prime_power(m)
    if prime_power:
        return True, p, n
    coprime_factors, m1, m2 = find_coprime_factors(m)
    if coprime_factors:
        return False, m1, m2
    return "No valid factorization found"

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

# Нахождение диксретного алгоритма перебором
def discrete_log(base, value, mod):
    for x in range(mod):
        if pow(base, x, mod) == value:
            return x
    return None

# Вычисление дискретного логарифма через собственные подгруппы
def log_subgroups(g, h, m):
    m = m - 1
    flag, m1, m2 = check_m_factorization(m)
    if flag:
        x = discrete_log(g, h, m + 1)
        return x
    else:
        # print(g, m2, h, g ** m2 % (m + 1), h ** m2 % (m + 1), m + 1)
        # print(g, m1, h, g ** m1 % (m + 1), h ** m1 % (m + 1), m + 1)
        p = m + 1
        x_1 = discrete_log(g ** m2 % p, h ** m2 % p, p)
        x_2 = discrete_log(g ** m1 % p, h ** m1 % p, p)
        x = china_theorem([x_2, x_1], [m2, m1])
        return x

def input_data():
    g = input("Введите онование g = ").strip()
    h = input("Элемент группы h = ").strip()
    m = input("Порядок группы m = ").strip()
    while not (g.isdigit() and h.isdigit() and m.isdigit()):
        g = input("g = ").strip()
        h = input("h = ").strip()
        m = input("m = ").strip()
    return int(g), int(h), int(m)


if __name__ == "__main__":
    type_ = """Введите тип дискретного логарифмирования: \n
1 - Метод Гельфонда-Шенкса 
2 - ρ-метод Полларда 
3 - Метод вычисления дискретного логарифма с помощью сведения к собственным подгруппам 
4 - Использовать все алгоритмы
5 - Выход\n"""
    print(type_)
    param = None
    while param not in ["1", "2", "3", "4", "5"]:
        param = input(":>")
        match param:
            case "1":
                print("Метод Гельфонда-Шенкса")
                try:
                    g, h, m = input_data()
                    x = log_gelfond_shanks(g, h, m)
                    print("Ответ:", x)
                    print(f"Проверка g ^ x = h (mod m) => {g} ^ {x} = {h} (mod {m}) => {pow(g, x, m)} = {h % m}")
                except Exception as err:
                    print(err)
                    print("Дискретный логарифм не найден!")
                param = None

            case "2":

                print("ρ-метод Полларда")
                try:
                    g, h, m = input_data()
                    eps = float(input("Укажите e (0 < e < 1): "))
                    x = pollard_rho_discrete_log(g, h, m, eps)
                    print("Ответ:", x)
                    print(f"Проверка g ^ x = h (mod m) => {g} ^ {x} = {h} (mod {m}) => {pow(g, x, m)} = {h % m}")
                except Exception as err:
                    print(err)
                    print("Дискретный логарифм не найден!")
                param = None

            case "3":

                print("Метод вычисления дискретного логарифма с помощью сведения к собственным подгруппам")
                try:
                    g, h, m = input_data()
                    x = log_subgroups(g, h, m)
                    print("Ответ:", x)
                    print(f"Проверка g ^ x = h (mod m) => {g} ^ {x} = {h} (mod {m}) => {pow(g, x, m)} = {h % m}")
                except Exception:
                    print("Дискретный логарифм не найден!")
                param = None

            case "4":

                print("Вычисление с помощью всех алгоритмов")
                g, h, m = input_data()
                eps = float(input("Укажите e (0 < e < 1): "))
                print("1) Алгоритм Гельфонда")
                try:
                    x = log_gelfond_shanks(g, h, m)
                    print("Ответ:", x)
                    print(f"Проверка g ^ x = h (mod m) => {g} ^ {x} = {h} (mod {m}) => {pow(g, x, m)} = {h % m}")
                except Exception:
                    print("Дискретный логарифм не найден!")
                print("2) Алгоритм Полларда")
                try:
                    x = pollard_rho_discrete_log(g, h, m, eps)
                    if x == -1:
                        print("Дискретный логарифм не найден!")
                    else:
                        print("Ответ:", x)
                        print(f"Проверка g ^ x = h (mod m) => {g} ^ {x} = {h} (mod {m}) => {pow(g, x, m)} = {h % m}")
                except Exception:
                    print("Дискретный логарифм не найден!")
                print("3) Вычисление через собственные подгруппы")
                try:
                    x = log_subgroups(g, h, m)
                    print("Ответ:", x)
                    print(f"Проверка g ^ x = h (mod m) => {g} ^ {x} = {h} (mod {m}) => {pow(g, x, m)} = {h % m}")
                except Exception:
                    print("Дискретный логарифм не найден!")
                param = None


            case "5":
                param = "5"


    # print(log_gelfond_shanks(2, 23, 37))
    # print(log_gelfond_shanks(3, 13, 17))
    # print(log_gelfond_shanks(7, 167, 587))
    # print(log_gelfond_shanks(78, 765, 1579))
    # print(log_gelfond_shanks(2, 10, 19))
    # print(log_gelfond_shanks(2, 22, 29))
    
    # print("====================================")
    

    # print(pollard_rho_discrete_log(2, 23, 37))
    # print(pollard_rho_discrete_log(3, 13, 17))
    # print(pollard_rho_discrete_log(7, 167, 587))
    # print(pollard_rho_discrete_log(78, 765, 1579))
    # print(pollard_rho_discrete_log(2, 10, 19))
    # print(pollard_rho_discrete_log(2, 22, 29))

    # print("====================================")

    # print(log_subgroups(2, 23, 37))
    # print(log_subgroups(3, 13, 17))
    # print(log_subgroups(7, 167, 587))
    # print(log_subgroups(78, 765, 1579))
    # print(log_subgroups(2, 10, 19))
    # print(log_subgroups(2, 22, 29))
    # print(log_subgroups(2, 22, 9997))

    #print(pollards_rho_discrete_log(7, 167, 587))
