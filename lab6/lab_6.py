import math
import cmath

# Прямое дискретное преобразование Фурье (DFT)
def DFT(lst_vals):
    N = len(lst_vals)
    result = []
    for k in range(N):
        X_k = 0
        for n in range(N):
            pow_ = -2 * math.pi * k * n / N
            X_k += lst_vals[n] * cmath.exp(1j * pow_)
        result.append(X_k)
    return result

# Быстрое дискретное преобразование
def FFT(a):
    n = len(a)
    if n <= 1:
        return a

    # Разделяем на четные и нечетные индексы
    even = FFT(a[0::2])
    odd = FFT(a[1::2])

    # Вычисляем корень из единицы
    T = [math.e**(-2j * math.pi * k / n) * odd[k] for k in range(n // 2)]
    
    # Собираем результаты
    return [even[k] + T[k] for k in range(n // 2)] + \
           [even[k] - T[k] for k in range(n // 2)]

# Быстрое обратное дискретное преобразование
def IFFT(a):
    n = len(a)
    if n <= 1:
        return a
    a_conj = [x.conjugate() for x in a]
    y = FFT(a_conj)
    return [x.conjugate() / n for x in y]

# Проверяем на длину массива
def power_of_two(a):
    n = len(a)
    power_ = 1
    while power_ < n:
        power_ *= 2
    return a + [0] * (power_ - n)

# Обратное дискретное преобразование Фурье (IDFT)
def IDFT(lst_spectr):
    N = len(lst_spectr)
    result = []
    for n in range(N):
        x_n = 0
        for k in range(N):
            pow_ = 2 * math.pi * k * n / N
            x_n += lst_spectr[k] * cmath.exp(1j * pow_)
        result.append(x_n / N)
    return result

# Основной алгоритм для произведения многочленов с использованием DFT и IDFT
def mul_polinom(A, B):
    n = 1
    while n < len(A) + len(B):
        n *= 2
    A += [0] * (n - len(A))
    B += [0] * (n - len(B))
    FA = DFT(A)
    FB = DFT(B)
    FC = [FA[i] * FB[i] for i in range(n)]
    C = IDFT(FC)
    return [round(c.real) for c in C]

# Алгоритм Шенхаге-Штрассена для умножения больших чисел
def mul(x, y):
   
    a = [int(digit) for digit in str(x)][::-1]
    b = [int(digit) for digit in str(y)][::-1]
    
    product = mul_polinom(a, b)
    
    carry = 0
    result = []
    for coeff in product:
        total = coeff + carry
        result.append(total % 10)
        carry = total // 10
    
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    
    return int(''.join(map(str, result[::-1])))

if __name__ == "__main__":
    type_ = """Введите тип операции: \n
1 - Вычисление прямого и обратного преобразования Фурье
2 - Вычисление быстрого прямого и обратного преобразования Фурье
3 - Умножение двух многочленов A и B с помощью дискретного преобразования Фурье  
4 - Умножение больших чисел методом дискретного преобразования Фурье
5 - Выход\n"""
    print(type_)
    param = None
    while param not in ["1", "2", "3", "4"]:
        param = input(":>")
        match param:
            case "1":
                print("Вычисление прямого и обратного преобразования Фурье")
                lst = list(map(lambda x: int(x), input("Укажите список дискретных значений: ").split()))
                spectrum = DFT(lst)
                recovered_lst = IDFT(spectrum)
                print("Исходная последовательность:", lst)
                print("Спектральное представление (DFT):", spectrum)
                print("Восстановленная последовательность до преобразования: ", recovered_lst)
                print("Восстановленная последовательность (IDFT):", [round(x.real) for x in recovered_lst])
                param = None
            case "2":
                print("Вычисление быстрого прямого и обратного преобразования Фурье")
                lst = list(map(lambda x: int(x), input("Укажите список дискретных значений: ").split()))
                len_ = len(lst)
                new_lst = power_of_two(lst)
                spectrum = FFT(new_lst)
                recovered_lst = IFFT(spectrum)
                print("Исходная последовательность:", lst)
                print("Спектральное представление (FFT):", spectrum[:len_])
                print("Восстановленная последовательность до преобразования: ", recovered_lst[:len_])
                print("Восстановленная последовательность (IFFT):", [round(x.real) for x in recovered_lst[:len_]])
                param = None
            case "3":
                print("Умножение двух многочленов A и B с помощью дискретного преобразования Фурье")
                print("Укажите многочлены A и B (сначала старшие степени)")
                A = list(map(lambda x: int(x), input("A: ").split()))[::-1]
                B = list(map(lambda x: int(x), input("B: ").split()))[::-1]
                print(A, B)
                res = mul_polinom(A, B)[::-1]
                for i in range(len(res)):
                    if res[i] != 0:
                        break
                print(res[i:])
                param = None
            case "4":
                print("Умножение больших чисел методом дискретного преобразования Фурье")
                x = int(input("Введите число x: "))
                y = int(input("Введите число y: "))
                product = mul(x, y)
                print("Результат умножения x и у:", product)
                print(f"Проверка со встроенным умножением: {x * y}")
                param = None
            case "5":
                param = "4"