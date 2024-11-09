import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Тест Ферма
def ferma(n, k):
    if n < 1:
        return False
    if n <= 3:
        return True
    for _ in range(k):
        a = random.randint(2, n - 2)
        r = pow(a, n - 1, n)
        if r != 1: return False
    return True

# Функция для вычисления символа Якоби
def jacobi(a, n):
    assert n > 0 and n % 2 == 1
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

# Тест Соловея-Штрассена
def strassen(k, n):
    if n < 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 1)
        if gcd(a, n) > 1:
            return False
        if jacobi(a, n) % n != pow(a, (n - 1) // 2, n):
            return False
    return True

# n – 1 = 2^Sq
def divider(n):
    s = 0
    q = n - 1
    while q % 2 == 0:
        s += 1
        q //= 2
    return s, q

# a^((2^k)q) ≡ -1 (mod m) => -1 ≡ m - 1 (mod m)
def check(a, s, q, n):
    for i in range(s):
        if pow(a, pow(2, i) * q, n) == n - 1:
            return True
    return False

# Тест Робина-Миллера
def robin_miller(n, k=100):
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    else: 
        for _ in range(k):
            a = random.randint(2, n - 1)
            s, q = divider(n)
            if n % a != 0 and (pow(a, q, n) == 1 or check(a, s, q, n)):
                    continue
            else:
                return False
        return True 

if __name__ == "__main__":
    type_ = """Введите тип теста проверки числа на простоту: \n
1 - Тест Ферма
2 - Тест Соловея-Штрассена
3 - Тест Робина-Миллера 
4 - Протестировать все тесты\n"""
    print(type_)
    param = None
    while param not in ["1", "2", "3", "4"]:
        param = input(":>")
    n, k = "","" 
    while not (n.isdigit() and k.isdigit()):
        n = input("Введите число n, которые хотите проверить на простоту\nn = ").strip()
        k = input("Введите число k равное количеству раундов проверки\nk = ").strip()
    match param:
        case "1":
            print("Тест Ферма")
            res = ferma(int(n), int(k))
            s = "Вероятно простое" if res else "Составное"
            print(f"Число {n} {s}")
        case "2":
            print("Тест Соловея-Штрассена")
            res = strassen(int(k), int(n))
            s = "Вероятно простое" if res else "Составное"
            print(f"Число {n} {s}")
        case "3":
            print("Тест Робина-Миллера")
            res = robin_miller(int(n), int(k))
            s = "Вероятно простое" if res else "Составное"
            print(f"Число {n} {s}")
        case "4":
            print("Тестирование всех тестов")
            res1 = ferma(int(n), int(k))
            res2 = strassen(int(k), int(n))
            res3 = robin_miller(int(n), int(k))
            s1 = "Вероятно простое" if res1 else "Составное"
            s2 = "Вероятно простое" if res2 else "Составное"
            s3 = "Вероятно простое" if res3 else "Составное"
            print(f"Тест Ферма: Число {n} {s1}\nТест Соловея-Штрассена: Число {n} {s2}\nТест Робина-Миллера: Число {n} {s2}\n")