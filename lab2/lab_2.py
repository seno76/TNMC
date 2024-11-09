import sympy

# Обычный алгоритм Евклида (НОД двух чисел) 
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# Цепная дробь
def chain_div(a, b):
    if a < b:
        a, b = b, a
    res = []
    while b:
        div_ = a // b
        res.append(div_)
        a, b = b, a % b
    return res


# Вычисление подходящих дробей
def suitable_fractions(a, b):
    P = [0, 1]
    Q = [1, 0]
    while b:
        q = a // b
        P.append(q * P[-1] + P[-2])
        Q.append(q * Q[-1] + Q[-2])
        a, b = b, a % b
    return P, Q


# Решение Диофантового уравнения
def diofant(a, b, c):
    gcd_ = gcd(a, b)
    if c % gcd_ == 0:
        a, b, c = a // gcd_, b // gcd_, c // gcd_
        P, Q = suitable_fractions(a, b)
        k = len(P)
        x = pow(-1, k) * c * Q[-2]
        y = pow(-1, k) * c * P[-2]
    else:
        return None, None
    return x, y


# Общее решение Диофантового уравнения
def diofant_global(a, b, x, y, t):
    return x + b * t, y + a * t


# Решение линейных сравнений
def system_comparisons(a, b, n):
    x, _ = diofant(a, n, b)
    return x


# Получение обратного элемента 
def inv_el(a, m):
    x, _ = diofant(a, m, 1)
    return x

def legendre(a, p):
    if not sympy.isprime(p):
        return None
    def legendre_recursive(a, p):
        if a < 0:
            if p % 4 == 1:
                return legendre_recursive(-a, p)
            else:
                return -legendre_recursive(-a, p)
        a = a % p
        if a == 0:
            return 0
        if a == 1:
            return 1
        if a == 2:
            if p % 8 == 1 or p % 8 == 7:
                return 1
            else:
                return -1
        if a % 2 == 0:
            return legendre_recursive(2, p) * legendre_recursive(a // 2, p)
        if a % 2 == 1:
            if a % 4 == 3 and p % 4 == 3:
                return -legendre_recursive(p, a)
            else:
                return legendre_recursive(p, a)
    
    return legendre_recursive(a, p)
    
# Символ Якоби 
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


# Извлечение квадратного корня в кольце вычетов
def mod_sqrt(a, p):
    if jacobi(a, p) != 1:
        return None, None 
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return r, p - r
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while jacobi(z, p) != -1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        t_pow = t
        i = 0
        for i in range(1, m):
            t_pow = pow(t_pow, 2, p)
            if t_pow == 1:
                break
        b = pow(c, pow(2, (m - i - 1)), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    return r, p - r


if __name__ == "__main__":
    type_ = print("""
Укажите номер операции:
1 - Разложение дроби вида a / b в цепную
2 - Вычисление подходящих дробей
3 - Решение Диофантового уравнения
4 - Решение линейных сравнений
5 - Вычисление обратного элемента в кольце вычетов             
6 - Вычисление символа Лежандра и Якоби
7 - Извлечение квадратного корня в кольце вычетов
8 - Выход""")
    param = None
    while param not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        param = input(":>").strip()
        match param:
            case "1":
                print("Выбрано: Разложение дроби вида a / b в цепную")
                while not ((a := input("a = ").strip()).isdigit()):
                    a = input("a = ")
                while not ((b := input("b = ").strip()).isdigit()):
                    b = input("b = ")
                res = chain_div(int(a), int(b))
                print(f"Цепная дробь: {res}")
                param = None
            case "2":
                print("Выбрано: Вычисление подходящих дробей для дроби вида a / b")
                while not ((a := input("a = ").strip()).isdigit()):
                    a = input("a = ")
                while not ((b := input("b = ").strip()).isdigit()):
                    b = input("b = ")
                P, Q = suitable_fractions(int(a), int(b))
                print("Числители P: ", P)
                print("Знаменатели Q: ", Q)
                param = None
            case "3":
                print("Выбрано: Решение Диофантового уравнения вида ax - by = c")
                print("Укажите параметры а, b, c:")
                while not ((a := input("a = ").strip()).isdigit()):
                    a = input("a = ")
                while not ((b := input("b = ").strip()).isdigit()):
                    b = input("b = ")
                while not ((c := input("c = ").strip()).isdigit()):
                    c = input("c = ")
                x, y = diofant(int(a), int(b), int(c))
                if x is None:
                    print(f"Решений нет")
                else:
                    print(f"x = {x}, y = {y}")
                    print(f"Проверка для уравнения {a}*x - {b}*y = {c} => {a}*{x} - {b}*{y} = {c}")
                    print(f"{int(a) * x - int(b) * y} = {c}")
                    flag = input("Хотите найти решение для параметра t: 1 - Да, 2 - Нет: ")
                    if flag == "1":
                        t = input("t = ")
                        x1, y1 = diofant_global(int(a), int(b), x, y, int(t))
                        print(f"x = {x1}, y = {y1}")
                        print(f"Проверка для уравнения {a}*x - {b}*y = {c} => {a}*{x1} - {b}*{y1} = {c}")
                        print(f"{int(a) * x1 - int(b) * y1} = {c}")
                param = None
            case "4":
                print("Выбрано: Решение линейных сравнений вида ax = b (mod n)")
                print("Укажите параметры:")
                while not ((a := input("a = ").strip()).isdigit()):
                    a = input("a = ")
                while not ((b := input("b = ").strip()).isdigit()):
                    b = input("b = ")
                while not ((n := input("n = ").strip()).isdigit()):
                    n = input("n = ")
                x = system_comparisons(int(a), int(b), int(n))
                if x is None:
                    print("Нет решений")
                else:
                    print("x =", x)
                    print(f"Проверка {a} * x = {b} (mod {n}) => {a} * {x} = {b} (mod {n})")
                    print(f"{int(a) * x % int(n)} = {int(b) % int(n)}")
                param = None
            case "5":
                print("Выбрано: Вычисление обратного элемента в кольце вычетов")
                a = input("Обатное для a = ")
                m = input("По модулю m = ")
                while gcd(int(a), int(m)) != 1:
                    print(f"gcd({a}, {m}) != 1")
                    a = input("Обатное для a = ")
                    m = input("По модулю m = ")
                x = inv_el(int(a), int(m))
                print(f"Обратный элемент к {a} =", x % int(m))
                print(f"Проверка: {int(a) * x % int(m)} = 1")
                param = None
            case "6":
                print("Выбрано: Вычисление символа Лежандра и Якоби (a, p)")
                print("Укажите параметры a, p (для Лежандра должен быть простым): ")
                a = input("a = ")
                while not ((p := input("p = ").strip()).isdigit()):
                    p = input("p = ")
                if a.split()[0] == "-":
                    res1 = legendre(-int(a), int(p))
                    res2 = jacobi(-int(a), int(p))
                else:
                    res1 = legendre(int(a), int(p))
                    res2 = jacobi(int(a), int(p))
                if res1 is None:
                    res1 = "p - не простое"
                print(f"Символ Лежандра: {res1}")
                print(f"Символ Якоби: {res2}")
                param = None
            case "7":
                print("Выбрано: Извлечение квадратного корня в кольце вычетов")
                print("Алгоритм Шенкса: необходимо найти x такое, что x^2 = n (mod p), n - кв. вычет, p - нечет. простое число")
                print("Укажите параметры:")
                n = input("n = ")
                p = input("p = ")
                res1, res2 = mod_sqrt(int(n), int(p))
                if res1 is None:
                    print(f"n = {n} - не является кв.вычетом")
                else:
                    print(f"x1 = {res1}, x2 = {res2}")
                    print(f"Проверка:\n{res1**2 % int(p)} = {int(n) % int(p)}\n{res2**2 % int(p)} = {int(n) % int(p)}")
                param = None
            case "8":
                param = "8"