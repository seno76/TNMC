start_massage = """
Укажите один из режимов работы программы:

1 - НОД двух чисел (Алгоритм Евклида)
2 - НОД двух чисел (Бинарный алгоритм Евклида)
3 - НОД двух чисел + коэффициенты Безу (Расширенный алгоритм Евклида)
4 - Решение системы сравнений первой степени (Китайская теорема об остатках)
5 - Решение системы сравнений первой степени (Алгоритм Гарнера)
6 - Решение системы линейных уравнений над полем целых чисел (Алгоритм Гаусса)
"""

def check_params(params, moduls):
    if len(params) != len(moduls):
        return False
    for i in range(len(params)):
        if not (params[i].isdigit() and moduls[i].isdigit()):
            return False
    return True

def parse_file(filepath):
    with open(filepath, "r") as f:
        res = []
        m, system = None, []
        lines = f.readlines()
        for i, line in enumerate(lines):
            new_l = line.strip().split()
            if len(new_l) == 1 and i == 0:
                m = int(new_l[0])
                system = []
            if len(new_l) == 1 and i != 0:
                m = int(new_l[0])
                system = []
                res.append([m, system])
            else:
                system.append(list(map(lambda x: int(x), new_l)))
    return res
            
