from pathlib import Path

from sympy import Expr, Integer, Symbol

from woke.ast.b_solc.c_ast_nodes import (
    AstSolc,
    SolcContractDefinition,
    SolcFunctionDefinition,
)
from woke.compile import (
    SolcOutput,
    SolcOutputContractInfo,
    SolcOutputSelectionEnum,
    SolidityCompiler,
)
from woke.compile.solc_frontend import SolcOutputErrorSeverityEnum
from woke.config import WokeConfig
from woke.regex_parsing import SolidityVersion
from woke.symbolic_execution.ast.engine import AstExecutionEngine


async def test_function():
    config = WokeConfig()
    compiler = SolidityCompiler(config, [Path(__file__).parent / "solidity_sources" / "Add.sol"])
    result = await compiler.compile([SolcOutputSelectionEnum.ALL], write_artifacts=False)
    out: SolcOutput = result[0]
    if out.errors is not None:
        for error in out.errors:
            if error.severity == SolcOutputErrorSeverityEnum.ERROR:
                raise Exception(error.message)

    for _, data in out.sources.items():
        ast = AstSolc.parse_obj(data.ast)

        for contract in (node for node in ast.nodes if isinstance(node, SolcContractDefinition)):
            for function in (node for node in contract.nodes if isinstance(node, SolcFunctionDefinition)):
                if function.name == "test":
                    engine = AstExecutionEngine()
                    print(engine.run(function, SolidityVersion.fromstring("0.8.7"), {"a": 10, "b": Symbol("x")}))
