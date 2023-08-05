from collections import defaultdict
from typing import DefaultDict, List

from woke.ast.b_solc.c_ast_nodes import AstSolc, SolcFunctionDefinition
from woke.build_artifacts_parser import BrownieContractArtifacts


class Resolver:
    __brownie_artifacts: List[BrownieContractArtifacts]
    __functions: DefaultDict[str, SolcFunctionDefinition]

    def __init__(self, brownie_artifacts: List[BrownieContractArtifacts]):
        self.__brownie_artifacts = list(brownie_artifacts)
        self.__functions = defaultdict(None)

    def setup(self):
        for artifact in self.__brownie_artifacts:
            ast = AstSolc.parse_obj(artifact.ast)

            for node in ast:
                if isinstance(node, SolcFunctionDefinition):
                    self.__functions[node.function_selector] = node

    def resolve_function(self, selector: str) -> SolcFunctionDefinition:
        return self.__functions[selector]
