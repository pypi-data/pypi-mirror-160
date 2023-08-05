import ast
from ast import ClassDef, FunctionDef, Module
from typing import Union

import astor

from woke.ast.b_solc.c_ast_nodes import (
    AstSolc,
    SolcArrayTypeName,
    SolcContractDefinition,
    SolcElementaryTypeName,
    SolcEnumDefinition,
    SolcErrorDefinition,
    SolcEventDefinition,
    SolcFunctionDefinition,
    SolcFunctionTypeName,
    SolcMapping,
    SolcNode,
    SolcStructDefinition,
    SolcTypeNameUnion,
    SolcUserDefinedTypeName,
    SolcUserDefinedValueTypeDefinition,
    SolcVariableDeclaration,
)


def generate_types(root_node: AstSolc) -> None:
    generated_types = []
    for node in root_node.nodes:
        generated = _generate_from_solc_node(node)
        if generated is not None:
            generated_types.append(generated)

    if len(generated_types):
        body = [ast.ImportFrom(module="enum", names=[ast.alias(name="IntEnum", asname=None)], level=0)]
        body.extend(generated_types)

        module = Module(body=body, type_ignores=[])
        print(astor.to_source(module))


def _generate_from_solc_node(node: SolcNode) -> Union[ClassDef, FunctionDef, ast.AnnAssign, None]:
    if isinstance(node, SolcEnumDefinition):
        return _generate_enum(node)
    elif isinstance(node, SolcFunctionDefinition):
        return _generate_function(node)
    elif isinstance(node, SolcStructDefinition):
        return _generate_struct(node)
    elif isinstance(node, SolcErrorDefinition):
        return _generate_error(node)
    elif isinstance(node, SolcContractDefinition):
        return _generate_contract(node)
    elif isinstance(node, SolcEventDefinition):
        return _generate_event(node)
    elif isinstance(node, SolcVariableDeclaration):
        return _generate_variable(node)
    else:
        return None


def _generate_enum(enum_definition: SolcEnumDefinition) -> ClassDef:
    values = []
    for num, member in enumerate(enum_definition.members):
        values.append(ast.Assign(
            # TODO check member.name.upper() is a valid Python identifier
            targets=[ast.Name(id=member.name.upper(), ctx=ast.Store())],
            value=ast.Num(n=num)
        ))

    return ClassDef(
        name=enum_definition.name,
        bases=[ast.Name(id="IntEnum", ctx=ast.Load())],
        keywords=[],
        body=values,
        decorator_list=[]
    )


def _generate_function(function_definition: SolcFunctionDefinition) -> FunctionDef:
    return FunctionDef()


def _generate_struct(struct_definition: SolcStructDefinition) -> ClassDef:
    variables = []
    for variable in struct_definition.members:
        variables.append(_generate_variable(variable))

    return ClassDef(
        name=struct_definition.name,
        bases=[],
        keywords=[],
        body=variables,
        decorator_list=[ast.Name(id="dataclass", ctx=ast.Load())]
    )


# TODO consider also FunctionDef instead of ClassDef
def _generate_error(error_definition: SolcErrorDefinition) -> ClassDef:
    return ClassDef()


# TODO wtf is this
def _generate_user_defined_type(user_defined_type_definition: SolcUserDefinedValueTypeDefinition) -> None:
    raise NotImplementedError()


def _generate_contract(contract_definition: SolcContractDefinition) -> ClassDef:
    return ClassDef()


# TODO consider also FunctionDef instead of ClassDef
def _generate_event(event_definition: SolcEventDefinition) -> ClassDef:
    return ClassDef()


def _generate_variable(variable_declaration: SolcVariableDeclaration) -> ast.AnnAssign:
    value = None  # TODO handle default values of state variables

    return ast.AnnAssign(
        target=ast.Name(id=variable_declaration.name, ctx=ast.Store()),  # TODO check this is a valid Python identifier
        annotation=_convert_type_name(variable_declaration.type_name),  # TODO variable_declaration.type_name may be None
        value=value,
        simple=True  # TODO check this
    )


def _convert_type_name(solc_type_name: SolcTypeNameUnion) -> Union[ast.Name, ast.Subscript]:
    if isinstance(solc_type_name, SolcArrayTypeName):
        return _get_array_type_name(solc_type_name)
    elif isinstance(solc_type_name, SolcElementaryTypeName):
        return _get_elementary_type_name(solc_type_name)
    elif isinstance(solc_type_name, SolcFunctionTypeName):
        raise NotImplementedError()
    elif isinstance(solc_type_name, SolcMapping):
        return _get_mapping_type_name(solc_type_name)
    elif isinstance(solc_type_name, SolcUserDefinedTypeName):
        raise NotImplementedError()
    else:
        raise NotImplementedError()


def _get_array_type_name(array_type_name: SolcArrayTypeName) -> ast.Subscript:
    # TODO handle fixed size arrays
    return ast.Subscript(
        value=ast.Name(id="List", ctx=ast.Load()),
        slice=ast.Index(value=_convert_type_name(array_type_name.base_type), ctx=ast.Load()),
        ctx=ast.Load()
    )


def _get_elementary_type_name(elementary_type_name: SolcElementaryTypeName) -> ast.Name:
    type_name = elementary_type_name.name
    if type_name == "string":
        python_type = "str"
    elif type_name in {"uint256", "uint128", "uint64", "uint32", "uint16", "uint8", "uint", "int256", "int128", "int64", "int32", "int16", "int8", "int"}:
        python_type = "int"  # TODO
    elif type_name == "bool":
        python_type = "bool"
    elif type_name == "address":
        python_type = "int"  # TODO
    else:
        raise NotImplementedError(
            f"Solidity type `{elementary_type_name.name}` not implemented."
        )
    return ast.Name(id=python_type, ctx=ast.Load())


def _get_mapping_type_name(mapping_type_name: SolcMapping) -> ast.Subscript:
    key_type = _convert_type_name(mapping_type_name.key_type)
    value_type = _convert_type_name(mapping_type_name.value_type)

    return ast.Subscript(
        value=ast.Name(id="Dict", ctx=ast.Load()),
        slice=ast.Index(
            value=ast.Tuple(elts=[key_type, value_type], ctx=ast.Load()),
            ctx=ast.Load()
        ),
        ctx=ast.Load()
    )
