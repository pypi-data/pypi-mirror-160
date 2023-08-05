import subprocess
from pathlib import Path

from woke.ast.b_solc.c_ast_nodes import AstSolc


def compile(path: Path) -> None:
    args = ["solc", "--ast-compact-json", str(path)]
    output = subprocess.check_output(args, stderr=subprocess.PIPE)
    lines = output.splitlines(True)

    json_path = Path(str(path).replace(".sol", ".json"))
    json_path.write_bytes(b"".join(lines[4:]))


def test_ast():
    print("")
    sources_path = Path(__file__).parent.resolve() / "solidity_sources"

    for f in sources_path.rglob("*.sol"):
        print(f"Compiling {f.name}")
        compile(f)

    for f in sources_path.rglob("*.json"):
        print(f"Parsing {f.name}")
        AstSolc.parse_file(f)


class X:
    @property
    def y(self) -> int:
        return 5


def test_tmp():
    print(X.abc)
