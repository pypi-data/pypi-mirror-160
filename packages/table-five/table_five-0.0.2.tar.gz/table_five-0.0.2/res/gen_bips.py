from functools import reduce


def bip(x):
    return min(0b11111 ^ x, x)

def reorder(a, b):
    if a > b:
        return b, a
    else:
        return a, b

def normalize_bips(a, b):
    a, b = bip(a), bip(b)
    a, b = reorder(a, b)
    return a, b

def get_bips(t):
    for n in t.traverse_postorder():
        if n.is_leaf():
            i = 4 - (int(n.label) - 1)
            n.bip = 1 << i
        else:
            n.bip = reduce(lambda x, y: x | y, [c.bip for c in n.children])
    for n in t.traverse_postorder():
        if n.is_leaf():
            continue
        if n.is_root():
            continue
        yield bip(n.bip)

def generate_splits():
    import treeswift as ts
    trees = ts.read_tree_newick('res/quintets.tre')
    for i, t in enumerate(trees):
        t1, t2 = list(set([b for b in get_bips(t)]))
        t1, t2 = reorder(t1, t2)
        print(f"({bin(t1)}, {bin(t2)}) => {i},")
generate_splits()
# def regenerate_table5():
#     splits = [
#         [0b00111, 0b00011],
#         [0b00111, 0b00101],
#         [0b00111, 0b00110],
#         [0b01011, 0b00011],
#         [0b01011, 0b01001],
#         [0b01011, 0b00011],
#     ]