import logging
import random
import time
from pathlib import Path
from typing import Dict, FrozenSet, List, Set

import networkx as nx
from Cryptodome.Hash import BLAKE2b

from woke.ast.b_solc.c_ast_nodes import AstNodeId, AstSolc, SolcNode, SolcSourceUnit
from woke.compile.solc_frontend import SolcOutputSourceInfo
from woke.core.solidity_version import SolidityVersionRanges


class CompilationUnit:
    __unit_graph: nx.DiGraph
    __version_ranges: SolidityVersionRanges
    __blake2b_digest: bytes
    __source_unit_names_to_paths: Dict[str, Path]

    def __init__(self, unit_graph: nx.DiGraph, version_ranges: SolidityVersionRanges):
        self.__unit_graph = unit_graph
        self.__version_ranges = version_ranges
        self.__source_unit_names_to_paths = {}

        sorted_nodes = sorted(
            unit_graph, key=(lambda node: unit_graph.nodes[node]["source_unit_name"])
        )
        blake2 = BLAKE2b.new(digest_bits=256)

        for node in sorted_nodes:
            blake2.update(unit_graph.nodes[node]["hash"])
            self.__source_unit_names_to_paths[unit_graph.nodes[node]["source_unit_name"]] = node
        self.__blake2b_digest = blake2.digest()

    def __len__(self):
        return len(self.__unit_graph.nodes)

    def __str__(self):
        return "\n".join(str(path) for path in self.__unit_graph.nodes)

    def draw(self, path: Path):
        labels = {node: data["source_unit_name"] for node, data in self.__unit_graph.nodes.items()}
        relabeled_graph = nx.reverse(nx.relabel_nodes(self.__unit_graph, labels), False)
        nx.nx_pydot.write_dot(relabeled_graph, path)

    def set_asts(self, asts: Dict[str, SolcOutputSourceInfo]):
        assert len(asts) == len(self.graph.nodes)

        labels = {}
        for source_unit_name, data in asts.items():
            path = self.__source_unit_names_to_paths[source_unit_name]
            ast = AstSolc.parse_obj()
            labels[path] = AstSolc.parse_obj(data.ast)

        nx.set_node_attributes(self.__unit_graph, labels, "ast")

    @property
    def files(self) -> FrozenSet[Path]:
        return frozenset(self.__unit_graph.nodes)

    @property
    def source_unit_names(self) -> FrozenSet[str]:
        return frozenset(
            self.__unit_graph.nodes[node]["source_unit_name"]
            for node in self.__unit_graph.nodes
        )

    @property
    def versions(self) -> SolidityVersionRanges:
        return self.__version_ranges

    @property
    def blake2b_digest(self) -> bytes:
        return self.__blake2b_digest

    @property
    def blake2b_hexdigest(self) -> str:
        return self.blake2b_digest.hex()

    @property
    def graph(self) -> nx.DiGraph:
        return self.__unit_graph


class CompiledCompilationUnit:
    __graph: nx.DiGraph
    ast_nodes_by_ids: Dict[AstNodeId, SolcNode]
    ast_nodes_by_paths: Dict[Path, Set[AstNodeId]]
    ast_referenced_ids: Dict[AstNodeId, Set[AstNodeId]]

    def __init__(self, graph: nx.DiGraph):
        self.__graph = graph.copy()
        self.ast_nodes_by_ids = {}
        self.ast_nodes_by_paths = {}
        self.ast_referenced_ids = {}

        for path in self.__graph.nodes:
            self.ast_nodes_by_paths[path] = set()
            ast: SolcSourceUnit = self.__graph.nodes[path]["ast"]
            nodes_by_ids, referenced_ids = ast.process_solc_source_unit()

            self.ast_nodes_by_ids.update(nodes_by_ids)
            self.ast_nodes_by_paths[path].update(nodes_by_ids.keys())
            self.ast_referenced_ids.update(referenced_ids)

    @classmethod
    def from_compilation_unit(cls, compilation_unit: CompilationUnit) -> "CompiledCompilationUnit":
        return cls(compilation_unit.graph)

    def merge(self, other: "CompiledCompilationUnit") -> "CompiledCompilationUnit":
        # keep as many ASTs from this unit as possible
        start = time.perf_counter()
        self_files = set(self.__graph.nodes)
        other_files = set(other.graph.nodes)

        common_files = self_files.intersection(other_files)

        forbidden: Set[AstNodeId] = set(self.ast_nodes_by_ids.keys())
        mapping: Dict[AstNodeId, AstNodeId] = {}

        for file in other_files - common_files:
            for node_id in other.ast_nodes_by_paths[file]:
                if node_id in forbidden:
                    # generate a new ID for this node and prepare mapping to fix references
                    new_id = random.randint(1, 100000)
                    while new_id in forbidden:
                        new_id = random.randint(1, 100000)

                    mapping[node_id] = AstNodeId(new_id)

        for file in common_files:
            self_ids = self.ast_nodes_by_paths[file]
            other_ids = other.ast_nodes_by_paths[file]
            assert len(self_ids) == len(other_ids)

            for self_id, other_id in zip(self_ids, other_ids):
                assert other_id not in mapping
                mapping[other_id] = self_id

        for file in other_files - common_files:
            ast: AstSolc = other.graph.nodes[file]["ast"]
            if ast.id in mapping:
                ast.id = mapping[ast.id]
            ast.replace_ids(mapping)

            for node in ast:
                if node.id in mapping:
                    node.id = mapping[node.id]
                node.replace_ids(mapping)

        composed_graph = nx.compose(other.graph, self.graph)

        xyz = CompiledCompilationUnit(composed_graph)
        logging.warning(time.perf_counter() - start)
        return xyz


        x = time.perf_counter()
        other_ast_nodes_by_ids: Dict[AstNodeId, SolcNode] = {}
        other_ast_nodes_by_paths: Dict[Path, List[AstNodeId]] = {}
        # remap AST IDs in others AST so that (self AST IDs) intersection (other AST IDs) is an empty set
        for file in other_files:
            other_ast_nodes_by_paths[file] = []
            other_ast = other.graph.nodes[file]["ast"]

            if other_ast.id in mapping:
                other_ast.id = mapping[other_ast.id]
            other_ast.replace_ids(mapping)

            other_ast_nodes_by_ids[other_ast.id] = other_ast
            other_ast_nodes_by_paths[file].append(other_ast.id)

            for node in other_ast:
                if node.id in mapping:
                    node.id = mapping[node.id]
                    node.replace_ids(mapping)

                other_ast_nodes_by_ids[node.id] = node
                other_ast_nodes_by_paths[file].append(node.id)
        logging.warning(f"removing duplicate ids: {time.perf_counter() - x}")

        #assert set(self.ast_nodes_by_ids.keys()).isdisjoint(other_ast_nodes_by_ids.keys())

        mapping = {}

        for file in other_files - common_files:
            ast_iter = iter(other.graph.nodes[file]["ast"])
            try:
                while True:
                    node: SolcNode = next(ast_iter)
                    node.replace_ids(mapping)
            except StopIteration:
                pass

        composed_graph = nx.compose(other.graph, self.graph)

        xyz = CompiledCompilationUnit(composed_graph)
        logging.warning(time.perf_counter() - start)
        return xyz

    @property
    def graph(self) -> nx.DiGraph:
        return self.__graph
