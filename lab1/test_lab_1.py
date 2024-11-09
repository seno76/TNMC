import TNMC.lab1.lab_1 as lab_1
import math
from random import randint
from test_gauss import test

def is_coprime(a, b):
    return math.gcd(a, b) == 1

def generate_garner_coprimes(limit):
    coprimes = []
    for i in range(2, limit):
        is_coprime_with_all = True
        for j in coprimes:
            if not is_coprime(i, j):
                is_coprime_with_all = False
                break
        if is_coprime_with_all:
            coprimes.append(i)
    return coprimes


def test_gcd():
    for _ in range(20_000):
        a, b = randint(1, 1e20), randint(1, 1e20)
        res1 = lab_1.gcd(a, b)
        res2 = math.gcd(a, b)
        print(a, b, res1, res2)
        if res1 != res2:
            return False
    return True


def test_gcd_bin():
    for _ in range(20_000):
        a, b = randint(1, 1e20), randint(1, 1e20)
        res1 = lab_1.gcd_bin(a, b)
        res2 = math.gcd(a, b)
        print(a, b, res1, res2)
        if res1 != res2:
            return False
    return True


def test_gcd_xt():
    for _ in range(20_000_0):
        a, b = randint(1, 1000), randint(1, 1000)
        x, y, g = lab_1.gcd_xt(a, b)
        if x * a + y * b != g:
            return False
    return True

def test_func(params, mods, u):
    for i, u_i in enumerate(params):
        if u_i % mods[i] != u % mods[i]:
            return False
    return True


def test_china_theorem():
    for _ in range(20_000):
        rand_num = randint(10, 2_000)
        m = generate_garner_coprimes(rand_num)
        u = []
        for _ in range(len(m)):
            u.append(randint(5, 1_000_000))
        res = lab_1.china_theorem(u, m)
        if test_func(u, m, res):
            print("Complite!!")
        else:
            print(u, m, res)
    return True

def test_garner_alg():
    for _ in range(20_000):
        rand_num = randint(10, 2_000)
        m = generate_garner_coprimes(rand_num)
        u = []
        for _ in range(len(m)):
            u.append(randint(5, 1_000_000))
        res = lab_1.garner_alg(u, m)

        if test_func(u, m, res):
            print("Complite!!")
        else:
            print(u, m, res)
    return True

def get_system(a, b):
    for i in range(len(a)):
        a[i].append(b[i])
    return a

def test_gausse():
    count, bad = 0, 0 
    for i, dict_ in enumerate(test):
        a = dict_["a"]
        b = dict_["b"]
        system = get_system(a, b)
        m = dict_["m"]
        solutions = dict_["solutions"]
        roots = lab_1.gauss_mod(system, m)
        roots.sort()
        if solutions == roots:
            count += 1
            print(f"Test {i + 1}): Complite!!!")
        else:
            bad += 1
            print("NOOOOOO")
            print(dict_)
        print(count, bad)


if __name__ == "__main__":
    #print(test_gcd()())
    #print(test_gcd_bin())
    #print(test_gcd_xt())
    #print(generate_garner_coprimes(2000))
    #print(test_china_theorem())
    #print(test_garner_alg())
    test_gausse()
    # mat = [[0, 0, 1, 1, 0, 1], [0, 0, 0, 1, 1, 1]]
    # p = 2
    # sol = [
    #         [0, 0, 0, 1, 0],
    #         [0, 0, 1, 0, 1],
    #         [0, 1, 0, 1, 0],
    #         [0, 1, 1, 0, 1],
    #         [1, 0, 0, 1, 0],
    #         [1, 0, 1, 0, 1],
    #         [1, 1, 0, 1, 0],
    #         [1, 1, 1, 0, 1],
    #     ],

    # print(lab_1.gauss_mod(mat, p))
        # print(gcd(0, 6))
    # print(gcd_bin(0, 6))
    # print(gcd_xt(240, 46))
    # test1 = china_theorem([2, 45, 64, 12, 23, 5], [3, 17, 31, 71, 23, 77])
    # test2 = garner_alg([2, 45, 64, 12, 23, 5], [3, 17, 31, 71, 23, 77])

    # print(test_func([2, 45, 64, 12, 23, 5], [3, 17, 31, 71, 23, 77], test1))
    # print(test_func([2, 45, 64, 12, 23, 5], [3, 17, 31, 71, 23, 77], test2))
matrix = [[5, 3, 5, 3],
          [1, 6, 2, 1],
          [3, 6, 0, 2]
        ]
    
matrix1 = [
    [1, 2, 0, 4, 0],
    [0, 3, 0, 2, 4],
    [0, 1, 1, 1, 0]
]
    
    # print(sub_row([2, 45, 64, 12, 23, 5], [3, 17, 31, 71, 23, 77], 10))
    # print_matrix(matrix)
    # print_matrix(get_matrix_A_and_vector(matrix))
    # print(mul_row_on_num([5, 3, 5, 3], -1))
    # print(gauss_mod(matrix, 7))

mat1 = [[0, 0, 1, 1, 0, 1], 
            [0, 0, 0, 1, 1, 1]]
p = 2
sol = [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1],
            [1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1],
        ]
    #print_matrix(gauss_mod(mat1, 2))


mat2 = [[1, 1, 1, 2, 0], [0, 2, 0, 0, 2], [2, 2, 1, 2, 0]]
m = 3
sol = [[2, 1, 0, 0], [2, 1, 1, 1], [2, 1, 2, 2]]

    #print(gauss_mod(mat2, m))

mat3 = [[12, 10, 7, 3], [10, 2, 3, 2]]
m = 13
sol = [
        [0, 7, 9],
        [1, 1, 1],
        [2, 8, 6],
        [3, 2, 11],
        [4, 9, 3],
        [5, 3, 8],
        [6, 10, 0],
        [7, 4, 5],
        [8, 11, 10],
        [9, 5, 2],
        [10, 12, 7],
        [11, 6, 12],
        [12, 0, 4],
    ],
    #print_matrix(gauss_mod(mat3, m))

mat4 = [[8, 1, 5], [9, 3, 6]]
m = 11
sol = [[5, 9]]

#print(gauss_mod(mat4, m))

mat5 = [[0, 0, 1, 0], [1, 0, 0, 0]]
m = 3
solutions = [[0, 0, 0], [0, 1, 0], [0, 2, 0]]
#print(gauss_mod(mat5, m))



mat7 = [[1, 0, 1, 1, 1, 0, 0], 
        [1, 1, 1, 1, 0, 1, 1], 
        [1, 0, 1, 1, 0, 1, 1], 
        [0, 1, 0, 0, 1, 1, 1], 
        [0, 1, 1, 1, 0, 11, 1]]
m = 2 
sol = [[0, 0, 0, 1, 1], [0, 0, 1, 0, 1]]

    # print(strassen(5, 3))
    # print(strassen(5, 7))
    # print(strassen(5, 17))
    # print(strassen(7, 123))
    # print(strassen(5, 67))
    # print(strassen(5, 111))
    # print(strassen(5, 561))
    # print(strassen(5, 65537))
    # print(strassen(5, 1105))
    # print(strassen(5, 1729))
    # print(strassen(5, 2465))
    # print(strassen(5, 2821))
    # print(strassen(5, 6601))
    # print(strassen(5, 8911))
    # print(strassen(5, 10585))
    # print(strassen(5, 15841))
    # print(strassen(5, 2465))