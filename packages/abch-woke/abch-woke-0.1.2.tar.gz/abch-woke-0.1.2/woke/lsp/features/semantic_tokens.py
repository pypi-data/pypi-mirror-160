import enum
import logging
import re
from typing import List, Optional, Tuple, Union

from woke.ast.b_solc.b_ast_enums import LiteralKind
from woke.ast.b_solc.c_ast_nodes import (
    AstSolc,
    SolcContractDefinition,
    SolcFunctionDefinition,
    SolcInheritanceSpecifier,
    SolcLiteral,
    SolcNode,
    Src,
)
from woke.compile.source_unit_name_resolver import SourceUnitNameResolver
from woke.lsp.common_structures import (
    PartialResultParams,
    StaticRegistrationOptions,
    TextDocumentIdentifier,
    TextDocumentRegistrationOptions,
    WorkDoneProgressOptions,
    WorkDoneProgressParams,
)
from woke.lsp.context import LspContext
from woke.lsp.exceptions import LspError
from woke.lsp.protocol_structures import ErrorCodes

from ..lsp_data_model import LspModel

logger = logging.getLogger(__name__)


SEMANTIC_TOKENS_LEGEND = [
    "type", "class", "enum", "interface", "struct", "type_parameter", "parameter",
    "variable", "propery", "enumMember", "event", "function", "method", "macro",
    "keyword", "modifier", "comment", "string", "number", "regexp", "operator",
    "decorator"
]


class SemanticTokenType(enum.IntEnum):
    TYPE = 0
    CLASS = 1
    ENUM = 2
    INTERFACE = 3
    STRUCT = 4
    TYPE_PARAMETER = 5
    PARAMETER = 6
    VARIABLE = 7
    PROPERTY = 8
    ENUM_MEMBER = 9
    EVENT = 10
    FUNCTION = 11
    METHOD = 12
    MACRO = 13
    KEYWORD = 14
    MODIFIER = 15
    COMMENT = 16
    STRING = 17
    NUMBER = 18
    REGEXP = 19
    OPERATOR = 20
    DECORATOR = 21


SEMANTIC_MODIFIERS_LEGEND = [
    "declaration", "definition", "readonly", "static", "deprecated", "abstract",
    "async", "modification", "documentation", "defaultLibrary"
]


class SemanticTokenModifier(enum.IntFlag):
    DECLARATION = 1
    DEFINITION = 2
    READONLY = 4
    STATIC = 8
    DEPRECATED = 16
    ABSTRACT = 32
    ASYNC = 64
    MODIFICATION = 128
    DOCUMENTATION = 256
    DEFAULT_LIBRARY = 512


class SemanticTokens(LspModel):
    result_id: Optional[str]
    """
    An optional result id. If provided and clients support delta updating
    the client will include the result id in the text semantic token request.
    A server can then instead of computing all semantic tokens again simply
    send a delta.
    """
    data: List[int]
    """
    The actual tokens.
    """


class SemanticTokensLegend(LspModel):
    token_types: List[str]
    """
    The token types a server uses.
    """
    token_modifiers: List[str]
    """
    The token modifiers a server uses.
    """


class SemanticTokensOptionsFull(LspModel):
    delta: Optional[bool]
    """
    The server supports deltas for full documents.
    """


class SemanticTokensOptions(WorkDoneProgressOptions):
    legend: SemanticTokensLegend
    """
    The legend used by the server
    """
    range: Optional[bool]
    """
    Server supports providing semantic tokens for a specific range
    of a document.
    """
    full: Optional[Union[bool, SemanticTokensOptionsFull]]
    """
    Server supports providing semantic tokens for a full document.
    """


class SemanticTokensRegistrationOptions(TextDocumentRegistrationOptions, SemanticTokensOptions, StaticRegistrationOptions):
    pass


class SemanticTokensParams(WorkDoneProgressParams, PartialResultParams):
    text_document: TextDocumentIdentifier
    """
    The text document.
    """


def _binary_search(lines: List[Tuple[bytes, int]], x: int) -> int:
    l = 0
    r = len(lines)

    while l < r:
        mid = l + (r - l) // 2
        if lines[mid][1] < x + 1:
            l = mid + 1
        else:
            r = mid

    return l - 1


IDENTIFIER = r"[a-zA-Z$_][a-zA-Z0-9$_]*"
IDENTIFIER_PATH = r"{identifier}(\.{identifier})*".format(identifier=IDENTIFIER)
CALL_ARGUMENT_LIST = r""
INHERITANCE_SPECIFIER = r"{identifier_path}({call_argument_list})?".format(identifier_path=IDENTIFIER_PATH, call_argument_list=CALL_ARGUMENT_LIST)

CONTRACT_RE = re.compile(r"^\s*((?P<abstract>abstract)\s)?\s*(?P<contract>contract)\s+(?P<name>{identifier})(\s+(?P<is>is))?".format(identifier=IDENTIFIER).encode("utf-8"))
INTERFACE_RE = re.compile(r"^\s*(?P<interface>interface)\s+(?P<name>{identifier})(\s+(?P<is>is))?".format(identifier=IDENTIFIER).encode("utf-8"))

INHERITANCE_SPECIFIER_RE = re.compile(r"^\s*(?P<name>{identifier_path})".format(identifier_path=IDENTIFIER_PATH).encode("utf-8"))


def _match_to_token(
        match: re.Match,
        group: str,
        byte_offset: int,
        type: SemanticTokenType,
        modifiers: List[SemanticTokenModifier]
) -> Tuple[int, int, SemanticTokenType, SemanticTokenModifier]:
    return byte_offset + match.start(group), match.end(group) - match.start(group), type, sum(modifiers)


def _inheritance_specifier_tokens(source: bytes, byte_offset: int) -> List[Tuple[int, int, int, int]]:
    inheritance_specifier_match = INHERITANCE_SPECIFIER_RE.match(source)
    assert inheritance_specifier_match
    # TODO SemanticTokenType here should be either CLASS or INTERFACE
    return [_match_to_token(inheritance_specifier_match, "name", byte_offset, SemanticTokenType.TYPE, [])]


def _contract_definition_tokens(source: bytes,
                                byte_offset: int) -> List[Tuple[int, int, int, int]]:
    contract_match = CONTRACT_RE.match(source)
    interface_match = INTERFACE_RE.match(source)
    assert contract_match or interface_match

    ret = []

    if contract_match:
        ret.append(_match_to_token(contract_match, "contract", byte_offset, SemanticTokenType.KEYWORD, []))

        if contract_match.group("abstract") is not None:
            ret.append(_match_to_token(contract_match, "abstract", byte_offset, SemanticTokenType.KEYWORD, []))
            ret.append(_match_to_token(contract_match, "name", byte_offset, SemanticTokenType.CLASS,
                                       [SemanticTokenModifier.ABSTRACT | SemanticTokenModifier.DEFINITION]))
        else:
            ret.append(_match_to_token(contract_match, "name", byte_offset, SemanticTokenType.CLASS,
                                       [SemanticTokenModifier.DEFINITION]))
        if contract_match.group("is") is not None:
            ret.append(_match_to_token(contract_match, "is", byte_offset, SemanticTokenType.KEYWORD, []))
    else:
        ret.append(_match_to_token(interface_match, "interface", byte_offset, SemanticTokenType.KEYWORD, []))
        ret.append(_match_to_token(interface_match, "name", byte_offset, SemanticTokenType.INTERFACE,
                                   [SemanticTokenModifier.DEFINITION]))
        if interface_match.group("is") is not None:
            ret.append(_match_to_token(interface_match, "is", byte_offset, SemanticTokenType.KEYWORD, []))
    return ret


def _literal_tokens(literal: SolcLiteral, source: bytes, byte_offset: int) -> List[Tuple[int, int, int, int]]:
    if literal.kind in {LiteralKind.STRING, LiteralKind.UNICODE_STRING, LiteralKind.HEX_STRING}:
        return [(literal.src.byte_offset, literal.src.byte_length, SemanticTokenType.STRING, 0)]
    elif literal.kind == LiteralKind.NUMBER:
        return [(literal.src.byte_offset, literal.src.byte_length, SemanticTokenType.NUMBER, 0)]
    elif literal.kind == LiteralKind.BOOL:
        return [(literal.src.byte_offset, literal.src.byte_length, SemanticTokenType.KEYWORD, 0)]


def _ast_node_to_semantic_tokens(node: SolcNode, source: bytes, byte_offset: int) -> List[Tuple[int, int, int, int]]:
    if isinstance(node, SolcContractDefinition):
        return _contract_definition_tokens(source, byte_offset)
    elif isinstance(node, SolcLiteral):
        return _literal_tokens(node, source, byte_offset)
    elif isinstance(node, SolcInheritanceSpecifier):
        return _inheritance_specifier_tokens(source, byte_offset)
    return []


def semantic_tokens_full(context: LspContext, params: SemanticTokensParams) -> Optional[SemanticTokens]:
    logger.info(f"Requested semantic tokens for file {params.text_document.uri}")
    context.compiler.output_ready.wait()

    path = context.compiler.uri_to_path(params.text_document.uri).resolve()
    source_unit_name_resolver = SourceUnitNameResolver(context.config)
    source_unit_name = source_unit_name_resolver.resolve_cmdline_arg(str(path))

    ast = None
    for out in context.compiler.output:
        if source_unit_name in out.sources:
            ast = AstSolc.parse_obj(out.sources[source_unit_name].ast)
            break

    if ast is None:
        logger.info(f"No AST found for file {params.text_document.uri}, {source_unit_name}")
        logger.info(f"Available ASTs: {[out.sources.keys() for out in context.compiler.output]}")
        raise LspError(ErrorCodes.RequestFailed, "Failed to compile the project.")

    source = context.compiler.get_compiled_file(params.text_document.uri)
    encoded_source = source.encode("utf-8")

    # [byte offset, type, modifiers]
    tokens: List[Tuple[int, int, int, int]] = []
    node: SolcNode
    for node in ast:
        node_tokens = _ast_node_to_semantic_tokens(
            node,
            encoded_source[node.src.byte_offset:(node.src.byte_offset + node.src.byte_length)],
            node.src.byte_offset
        )
        tokens.extend(node_tokens)

    tokens.sort(key=(lambda token: token[0]))

    tmp_lines = re.split(r"(\r?\n)", source)
    lines: List[str] = []
    for line in tmp_lines:
        if line in {"\r\n", "\n"}:
            lines[-1] += line
        else:
            lines.append(line)

    # UTF-8 encoded lines with prefix length
    encoded_lines: List[Tuple[bytes, int]] = []
    prefix_sum = 0
    for line in lines:
        encoded_line = line.encode("utf-8")
        encoded_lines.append((encoded_line, prefix_sum))
        prefix_sum += len(encoded_line)

    encoded_tokens = []
    last_line_num = 0
    last_start_char = 0

    for byte_offset, byte_length, semantic_type, semantic_modifiers in tokens:
        line_num = _binary_search(encoded_lines, byte_offset)
        line_data, prefix_sum = encoded_lines[line_num]
        line_offset = byte_offset - prefix_sum

        if line_num != last_line_num:
            last_start_char = 0

        start_char = len(line_data[:line_offset].decode("utf-8"))
        length = len(line_data[line_offset:(line_offset + byte_length)].decode("utf-8"))

        # delta line
        encoded_tokens.append(line_num - last_line_num)
        # delta start char
        encoded_tokens.append(start_char - last_start_char)
        # length
        encoded_tokens.append(length)
        # semantic type
        encoded_tokens.append(semantic_type)
        # semantic modifiers
        encoded_tokens.append(semantic_modifiers)

        last_line_num = line_num
        last_start_char = start_char

    logger.info(f"Encoded tokens: {encoded_tokens}")

    return SemanticTokens(
        data=encoded_tokens,
    )
