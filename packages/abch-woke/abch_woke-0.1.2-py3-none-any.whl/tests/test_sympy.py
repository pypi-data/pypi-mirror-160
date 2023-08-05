from sympy import Symbol
from sympy.core.add import Add


def test_sympy():
    x = Symbol("x")
    y = Symbol("2")
    z: Symbol = x + y
    print(type(z))

    x = Symbol("1")
    print(x / y)
