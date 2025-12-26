import networkx as nx
import matplotlib.pyplot as plt
import threading

# Globalny słownik, mnożniki obliczane na
# potrzeby odejmowania wierszy
mki = {}

# Globalny słownik, wartości pomnożone przez
# mnożniki na potrzeby odejmowania wierszy
nkij = {}

# Zadanie A, obliczenie mnożnika
def A(M: list[list[float]], i: int, k: int) -> None:
    mki[f"{k}_{i}"] = M[k - 1][i - 1] / M[i - 1][i - 1]

# Zadanie B, obliczenie pomnożonej wartości
def B(M: list[list[float]], i: int, j: int, k: int) -> None:
    nkij[f"{k}_{i}_{j}"] = M[i - 1][j - 1] * mki[f"{k}_{i}"]

# Zadanie C, wyzerowanie komórki
def C(M: list[list[float]], i: int, j: int, k: int) -> None:
    M[k - 1][j - 1] -= nkij[f"{k}_{i}_{j}"]

# Algorytm eliminacji Gaussa wykonany współbieżnie dzięki
# postaci normalnej Foaty
def parallel_gauss(matrix: list[list[float]], fnf: list[list[dict]]) -> list[list[float]]:
    M = [[e for e in row] for row in matrix]

    for f in fnf:
        thread_list = []

        for task in f:
            if task["operation"] == "A":
                thread_list.append(threading.Thread(target = A(M, task["i"], task["k"])))
            elif task["operation"] == "B":
                thread_list.append(threading.Thread(target = B(M, task["i"], task["j"], task["k"])))
            elif task["operation"] == "C":
                thread_list.append(threading.Thread(target = C(M, task["i"], task["j"], task["k"])))
        
        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()
    
    return M

# Sprowadzenie macierzy do postaci jednostkowej
def backward_substitution(eM: list[list[float]], n: int) -> list[float]:
    results = [0 for _ in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            eM[i][n] -= eM[i][j] * results[j]
            eM[i][j] = 0.0

        eM[i][n] /= eM[i][i]
        results[i] = eM[i][n]
        eM[i][i] = 1.0

    return results

# Przetwarzanie danych z pliku, zwraca krotkę (rozmiar macierzy, macierz, kolumna)
def process_file(file_path: str) -> tuple[int, list[list[float]], list[list[float]]]:
    with open(file_path, "r") as file:
        lines = file.read().split("\n")

        # Pierwszy wiersz - rozmiar macierzy
        n = int(lines[0])

        # Wiersze od drugiego do przedostatniego - macierz
        matrix = [[None for _ in range(n)] for _ in range(n)]

        for i in range(1, n + 1):
            row = lines[i].split(" ")
            for j in range(n):
                matrix[i - 1][j] = float(row[j])

        # Ostatni wiersz - transponowana kolumna
        column = [[None] for _ in range(n)]
        row = lines[n + 1].split(" ")

        for i in range(n):
            column[i][0] = float(row[i])

        return n, matrix, column

# Przedstawienie rodzaju operacji w postaci napisu
def print_operation(operation: dict) -> str:
    return f"A_({operation["i"]},{operation["k"]})" if operation["operation"] == "A" else \
           f"{operation["operation"]}_({operation["i"]},{operation["j"]},{operation["k"]})"

# Wyznaczanie alfabetu - operacji A, B i C na podstawie rozmiaru macierzy
def get_alphabet(n: int) -> tuple[list[dict], list[int]]:
    alphabet = []
    endlines = []

    for i in range(1, n):
        for k in range(i + 1, n + 1):
            alphabet.append({"operation": "A",
                             "i": i,
                             "k": k})

            for j in range(i, n + 2):
                alphabet.append({"operation": "B",
                                 "i": i,
                                 "j": j,
                                 "k": k})
                alphabet.append({"operation": "C",
                                 "i": i,
                                 "j": j,
                                 "k": k})
            
            if i < n - 1:
                if endlines:
                    endlines.append(endlines[-1] + 2 * (n + 2 - i) + 1)
                else:
                    endlines.append(2 * (n + 2 - i))

    return alphabet, endlines

# Wyznaczanie relacji zależności na podstawie rozmiaru macierzy
def get_dependent_transaction(n: int) -> tuple[list[dict], list[int]]:
    dependent = []
    endlines = []

    for i in range(1, n):
        for k in range(i + 1, n + 1):
            operation_A = {"operation": "A",
                           "i": i,
                           "k": k}
            
            for j in range(i, n + 2):
                operation_B = {"operation": "B",
                               "i": i,
                               "j": j,
                               "k": k}
                dependent.append((operation_A, operation_B))
            
            if endlines:
                endlines.append(endlines[-1] + n + 2 - i)
            else:
                endlines.append(n + 1 - i)

            for j in range(i, n + 2):
                operation_B = {"operation": "B",
                               "i": i,
                               "j": j,
                               "k": k}
                operation_C = {"operation": "C",
                               "i": i,
                               "j": j,
                               "k": k}
                dependent.append((operation_B, operation_C))
            
            endlines.append(endlines[-1] + n + 2 - i)
        
    for i in range(2, n):
        for k in range(i + 1, n + 1):
            operation_C1 = {"operation": "C",
                            "i": i - 1,
                            "j": i,
                            "k": i}
            operation_C2 = {"operation": "C",
                            "i": i - 1,
                            "j": i,
                            "k": k}
            operation_A = {"operation": "A",
                           "i": i,
                           "k": k}

            dependent.append((operation_C1, operation_A))
            dependent.append((operation_C2, operation_A))
    
        endlines.append(endlines[-1] + n + 1 - i)

        for k in range(i + 1, n + 1):
            for j in range(i + 1, n + 2):
                operation_C = {"operation": "C",
                               "i": i - 1,
                               "j": j,
                               "k": i}
                operation_B = {"operation": "B",
                               "i": i,
                               "j": j,
                               "k": k}
                dependent.append((operation_C, operation_B))

        endlines.append(endlines[-1] + n + 1 - i)

        for k in range(i + 1, n + 1):
            for j in range(i + 1, n + 2):
                operation_C1 = {"operation": "C",
                                "i": i - 1,
                                "j": j,
                                "k": k}
                operation_C2 = {"operation": "C",
                                "i": i,
                                "j": j,
                                "k": k}
                dependent.append((operation_C1, operation_C2))
        
        if i < n - 1:
            endlines.append(endlines[-1] + n + 1 - i)

    return dependent, endlines

# Wyznaczanie postaci normalnej Foaty
def get_fnf(n: int) -> list[list[dict]]:
    fnf = []

    for i in range(1, n):
        fnf.append([])

        for k in range(i + 1, n + 1):
            fnf[-1].append({"operation": "A",
                            "i": i,
                            "k": k})
            
        fnf.append([])

        for k in range(i + 1, n + 1):
            for j in range(i, n + 2):
                fnf[-1].append({"operation": "B",
                                "i": i,
                                "j": j,
                                "k": k})
                
        fnf.append([])

        for k in range(i + 1, n + 1):
            for j in range(i, n + 2):
                fnf[-1].append({"operation": "C",
                                "i": i,
                                "j": j,
                                "k": k})
    
    return fnf

# Wyznaczenie grafu i jego kolorów
def draw_graph(dependent: list[tuple[dict, dict]], fnf: list[list[dict]]) -> None:
    G = nx.DiGraph()

    node_colors = ["lime", "orange", "cyan", "pink"]

    max_len = max(len(f) for f in fnf)

    positions = {}
    colors = []

    for i in range(len(fnf)):
        shift_pos = max_len / len(fnf[i])
        base_pos = shift_pos / 2

        for j in range(len(fnf[i])):
            node = print_operation(fnf[i][j])
            G.add_node(node)
            positions[node] = [base_pos + j * shift_pos, 1 - i]
            colors.append(node_colors[i % 4])

    for dep in dependent:
        d1, d2 = dep
        node1 = print_operation(d1)
        node2 = print_operation(d2)
        G.add_edge(node1, node2)

    plt.figure(num = f"Graf zależności Diekerta wraz z kolorowaniem")
    nx.draw(G, positions, node_color = colors, width = 4, node_size = 5200)
    nx.draw_networkx_labels(G, positions, font_size = 16)
    plt.show()
