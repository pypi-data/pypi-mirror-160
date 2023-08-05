import logging
from typing import Union, List

from woke.ast.ir.abc import IrAbc
from woke.ast.ir.expression.identifier import Identifier
from woke.ast.ir.expression.member_access import MemberAccess
from woke.ast.ir.meta.identifier_path import IdentifierPath
from woke.ast.ir.type_name.user_defined_type_name import UserDefinedTypeName
from woke.lsp.common_structures import TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams, \
    Location, WorkDoneProgressOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions, Range, Position
from woke.lsp.context import LspContext
from woke.lsp.utils.uri import uri_to_path, path_to_uri

logger = logging.getLogger(__name__)


class DeclarationOptions(WorkDoneProgressOptions):
    pass


class DeclarationRegistrationOptions(DeclarationOptions, TextDocumentRegistrationOptions, StaticRegistrationOptions):
    pass


class DeclarationParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    pass


async def declaration(context: LspContext, params: DeclarationParams) -> Union[None, Location, List[Location]]:
    logger.info(f"Declaration for file {params.text_document.uri} at position {params.position} requested")
    await context.compiler.output_ready.wait()

    path = uri_to_path(params.text_document.uri).resolve()
    declarations = []

    if path in context.compiler.interval_trees:
        tree = context.compiler.interval_trees[path]

        byte_offset = context.compiler.get_byte_offset_from_line_pos(path, params.position.line, params.position.character)
        intervals = tree.at(byte_offset)
        nodes: List[IrAbc] = [interval.data for interval in intervals]
        logger.debug(f"Found {len(nodes)} nodes at byte offset {byte_offset}:\n{nodes}")

        node = max(nodes, key=lambda n: n.ast_tree_depth)
        logger.debug(f"Found node {node}")

        if isinstance(node, (Identifier, IdentifierPath, MemberAccess, UserDefinedTypeName)):
            referenced_declaration = node.referenced_declaration
            if referenced_declaration is None:
                return None
            uri = path_to_uri(referenced_declaration.file)

            declarations.append(Location(
                uri=uri,
                range=context.compiler.get_range_from_byte_offsets(referenced_declaration.file, referenced_declaration.name_location)
            ))
    return declarations
