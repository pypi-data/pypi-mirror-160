import ast


def test_python_enum():
    code = """
from enum import IntEnum


class Status(IntEnum):
    PENDING = 0
    SHIPPED = 1
    ACCEPTED = 2
    REJECTED = 3
    CANCELED = 4
    """

    tree = ast.parse(code, mode='exec')
    print(ast.dump(tree))


def test_python_struct():
    code = """
from dataclasses import dataclass

@dataclass
class Todo:
    text: str
    completed: bool
    xy: Dict[int, str]
    
    """

    tree = ast.parse(code, mode='exec')
    print(ast.dump(tree))
