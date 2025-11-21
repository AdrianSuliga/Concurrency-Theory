import networkx as nx

# input - str: transaction.txt path
# output - dict: map of variables used in a given transaction (symbol -> list of variables used) 
def get_transactions(transaction_file: str) -> dict[str, list[str]]:
    with open(transaction_file) as file:
        text = file.read()
        lines = text.split('\n')

        transactions = {}

        for line in lines:
            opening_idx = line.find("(")
            closing_idx = line.find(")")

            transaction_symbol = line[opening_idx + 1 : closing_idx]

            transactions[transaction_symbol] = []

            for idx in range(closing_idx + 1, len(line)):
                if 'a' <= line[idx] <= 'z':
                    transactions[transaction_symbol] += line[idx]
        
        return transactions

# input - str: alphabet.txt path
# output - list: alphabet sorted in alphabetical order
def get_alphabet(alphabet_file: str) -> list[str]:
    with open(alphabet_file) as file:
        text = file.read()
        alphabet = []

        for char in text:
            if 'a' <= char <= 'z':
                alphabet += char
        
        return sorted(alphabet)

# input - dict: transactions, result of get_transactions
#       - list: alphabet, result of get_alphabet
# output - bool: True if data is valid False otherwise
def verify_input(transactions:dict[str, list[str]], alphabet:list[str]) -> bool:
    return sorted(list(transactions.keys())) == alphabet

# input - list: alphabet, list of valid transactions
#       - str: word to check
# output - bool: True if word is valid False otherwise
def verify_word(alphabet:list[str], word: str) -> bool:
    for transaction in word:
        if transaction not in alphabet:
            return False
    
    return True

# input - dict: transactions, result of get_transactions
# output - set: set of dependent transactions
def get_dependent_transactions(transactions: dict[str, list[str]]) -> set[tuple[str, str]]:
    transaction_keys = transactions.keys()
    result = set()

    for outer_key in transaction_keys:
        left = transactions[outer_key][0]

        for inner_key in transaction_keys:
            for var in transactions[inner_key]:
                if left == var:
                    # mutually dependent
                    result.add((outer_key, inner_key))
                    result.add((inner_key, outer_key))
                    # no need for further search in the inner loop
                    break
    
    return result

# input - set: dependent transactions, result of get_dependent_transactions
#       - list: alphabet, result of get_alphabet
# output - dict: dependent transactions without redundant entries (symbol -> set of symbols)
def get_dependencies(dependent:set[tuple[str, str]], alphabet:list[str]) -> dict[set[str]]:
    result = {}

    for transaction in alphabet:
        result[transaction] = set()

    for first, second in dependent:
        if first is not second:
            result[first].add(second)
            result[second].add(first)
    
    return result

# helper function for fnf algorithm
def get_trans(trans_dict: dict[str, list[int]]) -> list[str]:
    result = []

    for key in trans_dict.keys():
        if trans_dict[key] and trans_dict[key][-1] == 1:
            trans_dict[key].pop()
            result.append(key)
    
    return result

# input - dict: dependencies, result of get_dependencies
#       - str: word to calculate fnf for
#       - list: alphabet, result of get_alphabet
# output - list: fnf for given word
def fnf_calculation(dependencies: dict[set[str]], word: str, alphabet: list[str]) -> list:
    trans_dict = {}
    for transaction in alphabet:
        trans_dict[transaction] = []

    for transaction in word[::-1]:
        trans_dict[transaction].append(1)

        for dep_trans in dependencies[transaction]:
            trans_dict[dep_trans].append(0)
    
    fnf = []

    while True:
        trans_list = get_trans(trans_dict)

        if not trans_list: break

        fnf.append(trans_list)

        for transaction in trans_list:
            for dependency in dependencies[transaction]:
                trans_dict[dependency].pop()
    
    return fnf

# input - dict: dependencies, result of get_dependencies
#       - str: word
# output - tuple: Graph, Positions and Labels
def get_graph(dependencies:dict[set[str]], word: str) -> tuple[nx.DiGraph, dict[str, list[int]], dict[str, str]]:
    edges = set()

    for i in range(len(word) - 1):
        for j in range(i + 1, len(word)):
            if word[j] in dependencies[word[i]] or word[i] == word[j]:
                edges.add((i + 1, j + 1))

    for i in range(1, len(word) - 1):
        for j in range(i + 1, len(word)):
            if (i, j) in edges:
                for k in range(j + 1, len(word) + 1):
                    if (i, k) in edges and (j, k) in edges:
                        edges.remove((i, k))

    G = nx.DiGraph()

    mappings = {}
    for i in range(len(word)):
        G.add_node(f"{word[i]}{i}")
        mappings[i + 1] = f"{word[i]}{i}"
    
    converted_edges = set()
    for u, v in edges:
        converted_edges.add((mappings[u], mappings[v]))

    G.add_edges_from(converted_edges)
    positions = {}
    labels = {}

    for i in range(len(word)):
        positions[f"{word[i]}{i}"] = [(-1) ** (i + 1), 1 - i // 2]
        labels[f"{word[i]}{i}"] = word[i]

    return G, positions, labels

