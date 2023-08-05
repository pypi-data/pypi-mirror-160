from typing import Any

from woke.ast.b_solc.c_ast_nodes import SolcTypeNameUnion, SolcVariableDeclaration

from ...ast.b_solc.b_ast_enums import StorageLocation
from ...cli.console import console
from .int_decoder import from_stack


def decode(x: bytes, variable_declaration: SolcVariableDeclaration) -> Any:
    if variable_declaration.storage_location == StorageLocation.MEMORY:
        pass
    #console.print_json(variable_declaration.json())
    return from_stack(x, variable_declaration.type_name)
