from typing import Dict, Tuple

from woke.ast.b_solc.c_ast_nodes import (
    AstSolc,
    SolcEnumDefinition,
    SolcErrorDefinition,
    SolcFunctionDefinition,
    SolcNode,
    SolcStructDefinition,
)
from woke.compile.solc_frontend import SolcOutputSourceInfo

from .types_generator import generate_types


def parse_ast(solc_output: Dict[str, SolcOutputSourceInfo]) -> Tuple[Dict[str, AstSolc], Dict[int, SolcNode]]:
    id_mapping = {}
    parsed_asts = {}

    for source_unit_name, raw_ast in solc_output.items():
        parsed_ast = AstSolc.parse_obj(raw_ast.ast)
        generate_types(parsed_ast)
        parsed_asts[source_unit_name] = parsed_ast
        id_mapping[parsed_ast.id] = parsed_ast

        for solc_node in parsed_ast:
            id_mapping[solc_node.id] = solc_node
    return parsed_asts, id_mapping




