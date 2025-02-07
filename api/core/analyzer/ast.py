import clang.cindex
import hashlib
from collections import Counter

clang.cindex.Config.set_library_file("/usr/lib/llvm-17/lib/libclang-17.so")


def parse_ast(code: str):
    index = clang.cindex.Index.create()
    tu = index.parse('temp.cpp', args=['-std=c++17'], unsaved_files=[('temp.cpp', code)])

    def traverse(node):
        node_data = f"Node: {node.kind} - {node.spelling}"
        node_hash = hashlib.md5(node_data.encode('utf-8')).hexdigest()
        return node_hash, [traverse(child) for child in node.get_children()]

    return traverse(tu.cursor)


def calculate_similarity(ast1, ast2):
    def flatten(ast):
        node_hashes, children = ast
        hashes = [node_hashes] + [flatten(child) for child in children]
        return [item for sublist in hashes for item in sublist]

    hashes1 = flatten(ast1)
    hashes2 = flatten(ast2)

    counter1 = Counter(hashes1)
    counter2 = Counter(hashes2)

    common = counter1 & counter2
    total = sum(common.values())

    total_nodes = len(hashes1) + len(hashes2) - total
    similarity = total / total_nodes if total_nodes > 0 else 1.0

    return similarity
