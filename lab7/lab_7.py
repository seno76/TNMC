import numpy as np

# Вывод матрицы в терминал
def print_matrix(matrix):
    for row in matrix:
        print(*row)
    print()

def gauss_reduce_lattice_2d(b1, b2):
    b1 = np.array(b1)
    b2 = np.array(b2)
    if np.linalg.norm(b1) > np.linalg.norm(b2):
        b1, b2 = b2, b1
    while True:
        dot_product = np.dot(b1, b2)
        norm_b1_squared = np.linalg.norm(b1) ** 2
        r = dot_product / norm_b1_squared + 0.5
        r_rounded = int(r + 0.1)
        a = b2 - r_rounded * b1
        if np.linalg.norm(a) ** 2 < np.linalg.norm(b1) ** 2:
            b1, b2 = a, b1
        else:
            return b1, a


def gram_schmidt(basis):
    d = len(basis)
    orthogonal_basis = np.zeros_like(basis)
    mu = np.zeros((d, d))
    
    for i in range(d):
        orthogonal_basis[i] = basis[i]
        for j in range(i):
            mu[i, j] = np.dot(basis[i], orthogonal_basis[j]) / \
                np.dot(orthogonal_basis[j], orthogonal_basis[j])
            orthogonal_basis[i] -= mu[i, j] * orthogonal_basis[j]
    
    return orthogonal_basis, mu

def update_mu(mu, basis, orthogonal_basis, k, d):
    for j in range(k):
        mu[k, j] = np.dot(basis[k], orthogonal_basis[j]) / \
            np.dot(orthogonal_basis[j], orthogonal_basis[j])

def lll_reduce(basis, delta=3/4):
    d = len(basis)
    basis = np.array(basis, dtype=float)
    
    orthogonal_basis, mu = gram_schmidt(basis)
    k = 1
    while k < d:
        for j in range(k - 1, -1, -1):
            if abs(mu[k, j]) > 0.5:
                r = round(mu[k, j])
                basis[k] -= r * basis[j]
                update_mu(mu, basis, orthogonal_basis, k, d)
        
        if np.dot(orthogonal_basis[k], orthogonal_basis[k]) >= (delta - mu[k, k - 1]**2) * \
                    np.dot(orthogonal_basis[k - 1], orthogonal_basis[k - 1]):
            k += 1
        else:
            basis[k], basis[k - 1] = basis[k - 1].copy(), basis[k].copy()
            orthogonal_basis, mu = gram_schmidt(basis)
            k = max(k - 1, 1)
    
    return basis

def gram_schmidt_1(B):
    """Ортогонализация базиса методом Грама-Шмидта."""
    B = np.array(B)
    N = B.shape[0]
    B_reduced = np.zeros_like(B, dtype=float)

    for i in range(N):
        B_reduced[i] = B[i]
        for j in range(i):
            B_reduced[i] -= np.dot(B[i], B_reduced[j]) / \
                np.dot(B_reduced[j], B_reduced[j]) * B_reduced[j]
    
    return B_reduced

def iterative_solve(solutions):
    """Итеративный перебор всех возможных решений в заданных границах."""
    N = len(solutions)
    stack = [[]]
    results = []
    
    while stack:
        current_sol = stack.pop()

        # Проверяем, если текущее решение содержит все координаты
        if len(current_sol) == N:
            results.append(current_sol)
        else:
            depth = len(current_sol)
            lower_bound, upper_bound = solutions[depth]

            # Добавляем новые возможные решения на стеке
            for z in range(lower_bound, upper_bound + 1):
                stack.append(current_sol + [z])

    return results

def find_solutions(C1, C2, B):
    """Нахождение всех решений на решетке в пределах границ C1 и C2."""
    N = len(B)
    
    # Шаг 1: Ортогонализация Грама-Шмидта
    B_reduced = gram_schmidt_1(B)
    
    # Шаг 2: Вычисляем границы для каждого измерения
    solutions = []
    for i in range(N):
        dot_product = np.dot(B_reduced[i], B_reduced.T)
        lower_bound = np.ceil((C1[i] - dot_product) / B_reduced[i][i]).astype(int)
        upper_bound = np.floor((C2[i] - dot_product) / B_reduced[i][i]).astype(int)
        
        lower_bound_scalar = lower_bound if np.isscalar(lower_bound) else lower_bound[0]
        upper_bound_scalar = upper_bound if np.isscalar(upper_bound) else upper_bound[0]
        
        solutions.append((lower_bound_scalar, upper_bound_scalar))

    # Шаг 3: Итерируем через возможные решения
    all_solutions = iterative_solve(solutions)

    # Шаг 4: Фильтруем решения по условиям C1 <= np.dot(B, sol) <= C2
    final_solutions = []
    for sol in all_solutions:
        sol_vector = np.dot(B, sol)
        if np.all(sol_vector >= C1) and np.all(sol_vector <= C2):
            final_solutions.append(sol)
    
    return final_solutions

if __name__ == "__main__":
    type_ = """Введите тип операции: \n
1 - Алгоритм Гаусса редукции решеток размерности 2
2 - Алгоритм Ленстры-Ленстры-Ловаша (LLL-алгоритм)
3 - Алгоритм решения задачи целочисленного программирования с помощью LLL-алгоритма
4 - Выход\n"""
    print(type_)
    param = None
    while param not in ["1", "2", "3", "4"]:
        param = input(":>")
        match param:
            case "1":
                print("Алгоритм Гаусса редукции решеток размерности 2")
                b1 = list(map(lambda x: int(x), input("Введите базис b1: ").split()))
                b2 = list(map(lambda x: int(x), input("Введите базис b2: ").split()))
                b1_reduced, b2_reduced = gauss_reduce_lattice_2d(b1, b2)
                print("Редуцированный базис:")
                print("b1:", *b1_reduced)
                print("b2:", *b2_reduced)
                param = None
            case "2":
                print("Алгоритм Ленстры-Ленстры-Ловаша (LLL-алгоритм)")
                k = int(input("Укажите количество базисов: "))
                lst = []
                for i in range(k):
                    b = list(map(lambda x: int(x), input(f"Введите базис {i + 1}: ").split()))
                    lst.append(b)
                reduced_basis = lll_reduce(lst)
                print("LLL-редуцированный базис:")
                print(reduced_basis)
                param = None
            case "3":
                print("Алгоритм решения задачи целочисленного программирования с помощью LLL-алгоритма")
                k = int(input("Укажите количество базисов: "))
                lst = []
                for i in range(k):
                    b = list(map(lambda x: int(x), input(f"Введите базис {i + 1}: ").split()))
                    lst.append(b)
                c1 = list(map(lambda x: int(x), input("Введите левые границы: ").split()))
                c2 = list(map(lambda x: int(x), input("Введите правые границы: ").split()))
                B = np.array(lst)
                C1 = np.array(c1)
                C2 = np.array(c2)
                solutions = find_solutions(C1, C2, B)
                print(solutions)
                for i, el in enumerate(solutions):
                    print(f"{i + 1})", el)
                param = None
            case "4":
                param = "4"