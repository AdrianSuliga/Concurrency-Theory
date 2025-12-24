import sys
import utils

def main() -> int:
    # Weryfikacja poprawności wywołania programu
    if len(sys.argv) != 3:
        print("Nieprawidłowa liczba argumentów. Oczekiwane wywołanie programu:")
        print("python3 main.py <ścieżka do pliku z danymi> <ścieżka do pliku z wynikiem>")
        sys.exit(1)

    # Wydobycie danych z pliku tekstowego
    n, matrix, column = utils.process_file(sys.argv[1])

    # Macierz uzupełniona o dodatkowy wektor
    complement_matrix = [row + element for row, element in zip(matrix, column)]

    # Wyznaczanie alfabetu z zadaniami A, B i C
    alphabet, endlines = utils.get_alphabet(n)
    print("Alfabet\nSigma = {", end = "")
    for i in range(len(alphabet)):
        print(utils.print_operation(alphabet[i]), end = "")
        if i < len(alphabet) - 1:
            print(",", end = " ")
        if i in endlines:
            print("\n         ", end = "")
    print("}")

    # Wyznaczanie relacji zależności
    dependent, dep_endlines = utils.get_dependent_transaction(n)
    print("\nRelacja zależności\nD = sym{{", end = "")
    for i in range(len(dependent)):
        dep1, dep2 = dependent[i]
        dep1_str = utils.print_operation(dep1)
        dep2_str = utils.print_operation(dep2)

        print(f"({dep1_str},{dep2_str})", end = "")

        if i < len(dependent) - 1:
            print(",", end = " ")
            if i in dep_endlines:
                print("\n         ", end = "")
    print("}^+} u I_Σ")

    # Wyznaczanie śladu wykonania algorytmu
    print("\nŚlad wykonania algorytmu\nw = ", end = "")
    for i in range(len(alphabet)):
        print(utils.print_operation(alphabet[i]), end = "")
        if i in endlines:
            print("\n    ", end = "")
    print()

    # Wyznaczanie postaci normalnej Foaty
    fnf = utils.get_fnf(n)
    print("\nPostać normalna Foaty\nFNF([w]) = ", end = "")
    for i in range(len(fnf)):
        print("[", end = "")
        for transaction in fnf[i]:
            print(utils.print_operation(transaction), end = "")
        print("]", end = "")
        if i % 2 == 1 and i < len(fnf) - 1:
            print("\n           ", end = "")
    print()

    # Przedstawienie grafu zależności
    utils.draw_graph(dependent, fnf)

    # Obliczenie rozwiązania
    eliminated_matrix = utils.parallel_gauss(complement_matrix, fnf)
    results = utils.backward_substitution(eliminated_matrix, n)

    # Jak wygląda macierz po rozwiązaniu układu
    print("\nMacierz po rozwiązaniu układu")
    print(*eliminated_matrix, sep = "\n")

    # Rozwiązanie 
    print("\nTransponowany wektor rozwiązań")
    print(results)

    # Zapis rozwiązania w postaci akceptowanej 
    # przez sprawdzarkę
    with open(sys.argv[2], "w") as f:
        s = str(n) + "\n"
        for row in eliminated_matrix:
            for i in range(len(row) - 1):
                s += str(row[i]) + " "
            s += "\n"
        for element in results:
            s += str(element) + " "
        s += "\n"
        f.write(s)

    return 0

if __name__ == "__main__":
    sys.exit(main())