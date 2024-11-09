from sympy import legendre_symbol, isprime, jacobi_symbol
from random import randint
import lab_2

def test_legendre_symbol(N):
    for i in range(100000):
        n = 4
        while not isprime(n):
            a = randint(1, N)
            n = randint(a+1, 2*N)
        
        j1 = lab_2.legendre(a, n)
        j2 = legendre_symbol(a, n)
        if j1 != j2:
            print(a, n, j1, j2)
            break
        else:
            print(f"{i + 1}) Complite!!")

def test_jacobi_symbol(N):
    for i in range(100000):
        a = randint(1, N)
        n = randint(a+1, 2*N)
        if n % 2 == 0:
            n += 1
        
        j1 = lab_2.jacobi(a, n)
        j2 = jacobi_symbol(a, n)

        if j1 != j2:
            print(a, n, j1, j2)
        else:
            print(f"{i + 1}) Complite!!")

# Функция для вычисления символа Лежандра
def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

# Функция для тестов
def test_modular_sqrt(test_count=10):
    # Генератор простых чисел
    def generate_prime(min_val, max_val):
        while True:
            p = randint(min_val, max_val)
            if isprime(p):
                return p

    # Генерация тестов
    for _ in range(test_count):
        # Генерируем случайное простое число p
        p = generate_prime(10, 1000)
        
        # Генерируем случайное число a в диапазоне от 0 до p-1
        a = randint(0, p-1)
        
        # Пытаемся найти квадратные корни
        result = lab_2.mod_sqrt(a, p)
        
        if result:
            r1, r2 = result
            print(f"Тест: a = {a}, p = {p}")
            print(f"Найденные корни: {r1}, {r2}")
            assert (r1 ** 2) % p == a and (r2 ** 2) % p == a, "Ошибка: корни неверны"
        else:
            print(f"Тест: a = {a}, p = {p}")
            print(f"Корней нет (ожидаемое поведение).")
        print("-" * 50)

 

if __name__ == "__main__":
    #test_legendre_symbol(1000)
    #test_jacobi_symbol(1000)
    test_modular_sqrt(10)

    # print(chain_div(62, 46))
    # print(gcd(46, 62))
    # print(chain_div(17, 323))
    # print(chain_div(8, 5))
    # print(suitable_fractions(8, 5))
    # print(suitable_fractions(19, 15))
    # print(diofant(19, 15, 11))
    # print(diofant(655, 115, 700))
    # print(diofant(31, 23, 11))
    # print(diofant_global(19, 15, 44, 55, 23))
    # print(system_comparisons(3, 5, 11))
    # print(inv_el(12, 13))
    # print(inv_el(14, 9))
    # print(jacobi(788888323, 78123123123))
    # print(legendre(98761, 1000))
    # print(legendre(88, 347))
    # print(mod_sqrt(5, 19))
    # print(mod_sqrt(186, 401))
    # print(mod_sqrt(10, 13)) 