import matplotlib.pyplot as plt
import networkx as nx
import sys
import util

def main() -> None:
    if len(sys.argv) != 4:
        print("Unexpected number of arguments. Expected format is:")
        print("python3 main.py <transaction_file> <alphabet_file> <word>")
        sys.exit(0)

    transaction_filename = sys.argv[1]
    alphabet_filename = sys.argv[2]
    word = sys.argv[3]

    transactions = util.get_transactions(transaction_filename)
    alphabet = util.get_alphabet(alphabet_filename)

    if not util.verify_input(transactions, alphabet):
        print("Text files data verification failed")
        sys.exit(0)

    if not util.verify_word(alphabet, word):
        print("Word verification failed")
        sys.exit(0)

    sigma = [(x, y) for y in alphabet for x in alphabet]
    dependent = sorted(list(util.get_dependent_transactions(transactions)))
    independent = sorted([item for item in sigma if not item in dependent])

    print("D = {", end = "")
    for i in range(len(dependent)):
        if i > 0: print(",", end = "")
        print(f"{dependent[i]}", end = "")
    print("}")

    print("I = {", end = "")
    for i in range(len(independent)):
        if i > 0: print(",", end = "")
        print(f"{independent[i]}", end = "")
    print("}")

    dependencies = util.get_dependencies(dependent, alphabet)
    fnf = util.fnf_calculation(dependencies, word, alphabet)
    print(f"FNF([{word}]) = ", end = "")
    for f in fnf:
        print("(", end = "")
        for transaction in sorted(f):
            print(transaction, end = "")
        print(")", end = "")
    print()

    G, positions, labels = util.get_graph(dependencies, word)
    plt.figure(num = f"Graf zależności dla słowa {word}")
    nx.draw(G, positions, labels = labels, with_labels = True,
            node_size = 600, connectionstyle = "arc3, rad = 0.20")
    plt.show()

if __name__ == "__main__":
    main()
