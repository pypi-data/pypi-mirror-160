import logging
import re
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from woke.compile.solc_frontend import SolcOutputErrorSeverityEnum
from woke.compile.source_unit_name_resolver import SourceUnitNameResolver
from woke.lsp.common_structures import (
    Diagnostic,
    DiagnosticSeverity,
    LspModel,
    PartialResultParams,
    Position,
    Range,
    StaticRegistrationOptions,
    TextDocumentIdentifier,
    TextDocumentRegistrationOptions,
    WorkDoneProgressOptions,
    WorkDoneProgressParams,
)
from woke.lsp.context import LspContext
from woke.lsp.utils.uri import uri_to_path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DocumentDiagnosticParams(WorkDoneProgressParams, PartialResultParams):
    text_document: TextDocumentIdentifier
    """
    The text document.
    """
    identifier: Optional[str]
    """
    The additional identifier provided during registration.
    """
    previous_result_id: Optional[str]
    """
    The result id of a previous response if provided.
    """


class DocumentDiagnosticReportKind(str, Enum):
    FULL = "full"
    """
    A full document diagnostic report.
    """
    UNCHANGED = "unchanged"
    """
    A report indicating that the last returned report is still accurate.
    """


class FullDocumentDiagnosticReport(LspModel):
    kind: DocumentDiagnosticReportKind = DocumentDiagnosticReportKind.FULL
    """
    A full document diagnostic report.
    """
    result_id: Optional[str]
    """
    An optional result id. If provided it will
    be sent on the next diagnostic request for the
    same document.
    """
    items: List[Diagnostic]


class UnchangedDocumentDiagnosticReport(LspModel):
    kind: DocumentDiagnosticReportKind = DocumentDiagnosticReportKind.UNCHANGED
    """
    A document diagnostic report indicating
    no changes to the last result. A server can
    only return `unchanged` if result ids are
    provided.
    """
    result_id: str
    """
    A result id which will be sent on the next
    diagnostic request for the same document.
    """


class RelatedFullDocumentDiagnosticReport(FullDocumentDiagnosticReport):
    related_documents: Optional[Dict[str, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]]]
    """
    Diagnostics of related document. The information is useful
    in programming languages where code in a file A can generate
    diagnostics in a file B which A depends on. An example of
    such a language is C/C++ where macro definitions in a file
    a.cpp and result in errors in a heder file b.hpp.
    """


class RelatedUnchangedDocumentDiagnosticReport(UnchangedDocumentDiagnosticReport):
    related_documents: Optional[Dict[str, Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]]]
    """
    Diagnostics of related document. The information is useful
    in programming languages where code in a file A can generate
    diagnostics in a file B which A depends on. An example of
    such a language is C/C++ where macro definitions in a file
    a.cpp and result in errors in a heder file b.hpp.
    """


DocumentDiagnosticReport = Union[RelatedFullDocumentDiagnosticReport, RelatedUnchangedDocumentDiagnosticReport]


class DiagnosticClientCapabilities(LspModel):
    dynamic_registration: Optional[bool]
    related_document_support: Optional[bool]


class DiagnosticOptions(WorkDoneProgressOptions):
    """
    Diagnostics options.
    """

    identifier: Optional[str] = None
    """
    An optional identifier under which the diagnostics are managed by the client.
    """
    inter_file_dependencies: bool
    """
    Whether the language has inter file dependencies meaning that
    editing code in one file can result in a different diagnostic
    set in another file. Inter file dependencies are common for
    most programming languages and typically uncommon for linters.
    """
    workspace_diagnostics: bool
    """
    The server provides support for workspace diagnostics as well.
    """


class DiagnosticRegistrationOptions(
    TextDocumentRegistrationOptions, DiagnosticOptions, StaticRegistrationOptions
):
    pass


def diagnostic(context: LspContext, params: DocumentDiagnosticParams) -> DocumentDiagnosticReport:
    """
    Return a list of diagnostics for the given file.
    """
    logger.info(f"Requested diagnostic for file {params.text_document.uri}")
    context.compiler.output_ready.wait()
    logger.info("Done waiting for compiler output")

    path = uri_to_path(params.text_document.uri).resolve()
    diagnostics: List[Diagnostic] = []

    for error in context.compiler.errors[path]:
        if error.source_location.start < 0 or error.source_location.end < 0:
            continue
        logger.info(f"Found error {error.message}")

        if error.severity == SolcOutputErrorSeverityEnum.ERROR:
            severity = DiagnosticSeverity.ERROR
        elif error.severity == SolcOutputErrorSeverityEnum.WARNING:
            severity = DiagnosticSeverity.WARNING
        elif error.severity == SolcOutputErrorSeverityEnum.INFO:
            severity = DiagnosticSeverity.INFORMATION
        else:
            raise ValueError()

        start = error.source_location.start
        end = error.source_location.end

        diagnostics.append(Diagnostic(
            range=context.compiler.get_range_from_byte_offsets(path, (start, end)),
            severity=severity,
            error_code=error.error_code,
            message=error.message,
        ))

    return RelatedFullDocumentDiagnosticReport(
        related_documents=None,
        items=diagnostics,
    )
