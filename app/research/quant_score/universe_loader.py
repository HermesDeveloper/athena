def load_symbols_from_txt(filepath):
    symbols = []

    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line and line != "Symbol" and "stock" not in line:
            symbols.append(line)

    return symbols
