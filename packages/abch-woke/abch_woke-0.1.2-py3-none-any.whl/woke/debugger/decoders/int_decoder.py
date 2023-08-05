from woke.ast.b_solc.c_ast_nodes import SolcElementaryTypeName


def from_stack(stack: bytes, type_name: SolcElementaryTypeName) -> int:
    return int.from_bytes(stack[:32], "big", signed=False)
