from collections import defaultdict, deque
from functools import partial
from itertools import chain
from typing import Callable, Tuple

import Cryptodome.Hash.keccak
import pytest

from woke.symbolic_execution.yul import BlockchainContext, YulExecutionContext
from woke.symbolic_execution.yul.containers import (
    CallData,
    Code,
    Memory,
    ReturnData,
    Stack,
    Storage,
)
from woke.symbolic_execution.yul.context import ChainIdEnum, ExecutionContextEnum
from woke.symbolic_execution.yul.instructions import *
from woke.symbolic_execution.yul.types import *

#Defaults = collections.namedtuple("Defaults", "storage memory call_data code return_data")
#
#
#@pytest.fixture
#def defaults():
#    d = Defaults(Storage(), Memory(), CallData(b""))
#    storage: Storage = Storage()
#    memory: Memory = Memory()
#    call_data: CallData = CallData(b"")
#    code: Code = Code(b"")
#    return_data = ReturnData(b"")
#    return storage, memory, call_data, code, return_data


def _unary_operation_helper(a: uint256, func: Callable[[Stack, YulExecutionContext], None]) -> uint256:
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    context = YulExecutionContext(storage, memory, call_data, code, return_data)
    stack: Stack = deque()
    stack.append(a)

    func(stack, context)
    return stack.pop()


def _binary_operation_helper(a: uint256, b: uint256, func: Callable[[Stack, YulExecutionContext], None]) -> uint256:
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    context = YulExecutionContext(storage, memory, call_data, code, return_data)
    stack: Stack = deque()
    stack.append(b)
    stack.append(a)

    func(stack, context)
    return stack.pop()


def _ternary_operation_helper(a: uint256, b: uint256, n: uint256, func: Callable[[Stack, YulExecutionContext], None]) -> uint256:
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    context = YulExecutionContext(storage, memory, call_data, code, return_data)
    stack: Stack = deque()
    stack.append(n)
    stack.append(b)
    stack.append(a)

    func(stack, context)
    return stack.pop()


def test_add():
    assert _binary_operation_helper(10, 10, evm_add) == 20
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 1, evm_add) == 0


def test_mul():
    assert _binary_operation_helper(10, 10, evm_mul) == 100
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 2, evm_mul) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE


def test_sub():
    assert _binary_operation_helper(10, 10, evm_sub) == 0
    assert _binary_operation_helper(0, 1, evm_sub) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


def test_div():
    assert _binary_operation_helper(10, 0, evm_div) == 0
    assert _binary_operation_helper(10, 10, evm_div) == 1
    assert _binary_operation_helper(1, 2, evm_div) == 0


def test_sdiv():
    assert _binary_operation_helper(10, 0, evm_sdiv) == 0
    assert _binary_operation_helper(10, 10, evm_sdiv) == 1
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE,
                                    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, evm_sdiv) == 2
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE, 1, evm_sdiv) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE


def test_mod():
    assert _binary_operation_helper(10, 0, evm_mod) == 0
    assert _binary_operation_helper(10, 3, evm_mod) == 1
    assert _binary_operation_helper(17, 5, evm_mod) == 2


def test_smod():
    assert _binary_operation_helper(10, 0, evm_smod) == 0
    assert _binary_operation_helper(10, 3, evm_smod) == 1
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8,
                                    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD, evm_smod) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE


def test_addmod():
    assert _ternary_operation_helper(10, 7, 0, evm_addmod) == 0
    assert _ternary_operation_helper(10, 10, 8, evm_addmod) == 4
    assert _ternary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 2, 2, evm_addmod) == 1


def test_mulmod():
    assert _ternary_operation_helper(10, 7, 0, evm_mulmod) == 0
    assert _ternary_operation_helper(10, 10, 8, evm_mulmod) == 4
    assert _ternary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
                                     0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 12, evm_mulmod) == 9


def test_exp():
    assert _binary_operation_helper(0, 0, evm_exp) == 1
    assert _binary_operation_helper(10, 2, evm_exp) == 100
    assert _binary_operation_helper(2, 2, evm_exp) == 4


def test_signextend():
    assert _binary_operation_helper(0, 0xFF, evm_signextend) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    assert _binary_operation_helper(1, 0x3F8F02, evm_signextend) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8F02
    assert _binary_operation_helper(0, 0x7F, evm_signextend) == 0x7F
    assert _binary_operation_helper(2, 0x877F350D, evm_signextend) == 0x7F350D


def test_lt():
    assert _binary_operation_helper(9, 10, evm_lt) == 1
    assert _binary_operation_helper(10, 10, evm_lt) == 0
    assert _binary_operation_helper(10, 9, evm_lt) == 0


def test_gt():
    assert _binary_operation_helper(9, 10, evm_gt) == 0
    assert _binary_operation_helper(10, 10, evm_gt) == 0
    assert _binary_operation_helper(10, 9, evm_gt) == 1


def test_slt():
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 0, evm_slt) == 1
    assert _binary_operation_helper(0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, evm_slt) == 0
    assert _binary_operation_helper(10, 10, evm_slt) == 0


def test_sgt():
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 0, evm_sgt) == 0
    assert _binary_operation_helper(0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, evm_sgt) == 1
    assert _binary_operation_helper(10, 10, evm_sgt) == 0


def test_eq():
    assert _binary_operation_helper(10, 7, evm_eq) == 0
    assert _binary_operation_helper(10, 10, evm_eq) == 1


def test_iszero():
    assert _unary_operation_helper(10, evm_iszero) == 0
    assert _unary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, evm_iszero) == 0
    assert _unary_operation_helper(0, evm_iszero) == 1


def test_and():
    assert _binary_operation_helper(0xF, 0xF, evm_and) == 0xF
    assert _binary_operation_helper(0xFF, 0, evm_and) == 0
    assert _binary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 0x30115f5de5a0, evm_and) == 0x30115f5de5a0


def test_or():
    assert _binary_operation_helper(0xF0, 0xF, evm_or) == 0xFF
    assert _binary_operation_helper(0xFF, 0xFF, evm_or) == 0xFF


def test_xor():
    assert _binary_operation_helper(0xF0, 0xF, evm_xor) == 0xFF
    assert _binary_operation_helper(0xFF, 0xFF, evm_xor) == 0


def test_not():
    assert _unary_operation_helper(0, evm_not) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    assert _unary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, evm_not) == 0
    assert _unary_operation_helper(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, evm_not) == 0
    assert _unary_operation_helper(0xF0F0F0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000, evm_not) == 0x0F0F0F000000000000000000000000000000000000000000000000000000FFFF
    assert _unary_operation_helper(0x0F0F0F000000000000000000000000000000000000000000000000000000FFFF, evm_not) == 0xF0F0F0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000


def test_byte():
    assert _binary_operation_helper(34, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, evm_byte) == 0
    assert _binary_operation_helper(31, 0xFF, evm_byte) == 0xFF
    assert _binary_operation_helper(30, 0xFF, evm_byte) == 0
    assert _binary_operation_helper(30, 0xFF00, evm_byte) == 0xFF
    assert _binary_operation_helper(0, 0x00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF, evm_byte) == 0
    assert _binary_operation_helper(1, 0x00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF, evm_byte) == 0x11
    assert _binary_operation_helper(10, 0x00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF, evm_byte) == 0xAA


def test_shl():
    assert _binary_operation_helper(1, 1, evm_shl) == 2
    assert _binary_operation_helper(4, 0xFF00000000000000000000000000000000000000000000000000000000000000, evm_shl) == 0xF000000000000000000000000000000000000000000000000000000000000000


def test_shr():
    assert _binary_operation_helper(1, 2, evm_shr) == 1
    assert _binary_operation_helper(4, 0xFF, evm_shr) == 0xF


def test_sar():
    assert _binary_operation_helper(1, 2, evm_sar) == 1
    assert _binary_operation_helper(4, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0, evm_sar) == 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


def test_keccak256():
    storage: Storage = Storage()
    memory: Memory = Memory()
    memory[0:4] = bytes([0xFF, 0xFF, 0xFF, 0xFF])
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    context = YulExecutionContext(storage, memory, call_data, code, return_data)
    stack: Stack = deque()

    # keccak256 hash of an empty sequence (length = 0)
    stack.append(0x0)
    stack.append(0x0)
    evm_keccak256(stack, context)
    assert stack.pop() == 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470

    stack.append(0x4)
    stack.append(0x0)
    evm_keccak256(stack, context)
    assert stack.pop() == 0x29045A592007D0C246EF02C2223570DA9522D0CF0F73282C79A1BC8F0BB2C238

    # out of bounds access
    stack.append(0x4)
    stack.append(0x3)
    evm_keccak256(stack, context)
    assert stack.pop() == 0x61251fc2178ac6bc09513e5dfe88f4402b7a6f554acd99c7940f608ff7e71433


def test_address():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data,
                                  self_address=0xB4F1f40304EA173A84C781B4Eed786b9Ca6a01eF)

    evm_address(stack, context)
    assert stack.pop() == 0xB4F1f40304EA173A84C781B4Eed786b9Ca6a01eF


def test_balance():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    balances = defaultdict(int)
    balances[0x3e192D3997E77e6d0272BaD5863790424f471048] = 123456
    context = YulExecutionContext(storage, memory, call_data, code, return_data, balances=balances)

    stack.append(0x3e192D3997E77e6d0272BaD5863790424f471048)
    evm_balance(stack, context)
    assert stack.pop() == 123456

    stack.append(0xB4F1f40304EA173A84C781B4Eed786b9Ca6a01eF)
    evm_balance(stack, context)
    assert stack.pop() == 0

    # new context without balances parameter
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(0x3e192D3997E77e6d0272BaD5863790424f471048)
    evm_balance(stack, context)
    assert stack.pop() == 0

    stack.append(0xB4F1f40304EA173A84C781B4Eed786b9Ca6a01eF)
    evm_balance(stack, context)
    assert stack.pop() == 0


def test_origin():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data,
                                  origin_address=0xa9CF62517e2D6B8E27E4D0Ee044bBBB628fE7EE1)

    evm_origin(stack, context)
    assert stack.pop() == 0xa9CF62517e2D6B8E27E4D0Ee044bBBB628fE7EE1


def test_caller():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data,
                                  caller_address=0x5B17238F57c61b2A0Dc7e7000DFdfe839F64C170)

    evm_caller(stack, context)
    assert stack.pop() == 0x5B17238F57c61b2A0Dc7e7000DFdfe839F64C170


def test_callvalue():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data, call_value=78305)

    evm_callvalue(stack, context)
    assert stack.pop() == 78305


def test_calldataload():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(i for i in range(16))
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(0)
    evm_calldataload(stack, context)
    assert stack.pop() == 0x000102030405060708090A0B0C0D0E0F00000000000000000000000000000000

    stack.append(1)
    evm_calldataload(stack, context)
    assert stack.pop() == 0x0102030405060708090A0B0C0D0E0F0000000000000000000000000000000000

    stack.append(2)
    evm_calldataload(stack, context)
    assert stack.pop() == 0x02030405060708090A0B0C0D0E0F000000000000000000000000000000000000


def test_calldatasize():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    evm_calldatasize(stack, context)
    assert stack.pop() == 0

    call_data: CallData = CallData(bytes(i for i in range(256)))
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    evm_calldatasize(stack, context)
    assert stack.pop() == 256

    call_data: CallData = CallData(bytes(i for i in range(32)))
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    evm_calldatasize(stack, context)
    assert stack.pop() == 32


def test_calldatacopy():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(i for i in range(16))
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(18)
    stack.append(0)
    stack.append(0)
    evm_calldatacopy(stack, context)
    assert context.memory[0:18] == bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x00, 0x00])

    stack.append(18)
    stack.append(1)
    stack.append(20)
    evm_calldatacopy(stack, context)
    assert context.memory[20:38] == bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x00, 0x00, 0x00])


def test_codesize():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()

    context = YulExecutionContext(storage, memory, call_data, code, return_data)
    evm_codesize(stack, context)
    assert stack.pop() == 0

    context = YulExecutionContext(storage, memory, call_data, Code(bytes(i for i in range(128))), return_data)
    evm_codesize(stack, context)
    assert stack.pop() == 128

    context = YulExecutionContext(storage, memory, call_data, Code(bytes(0 for _ in range(7830))), return_data)
    evm_codesize(stack, context)
    assert stack.pop() == 7830


def test_codecopy():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(i for i in range(16))
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(18)
    stack.append(0)
    stack.append(0)
    evm_codecopy(stack, context)
    assert context.memory[0:18] == bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x00, 0x00])

    stack.append(18)
    stack.append(1)
    stack.append(20)
    evm_codecopy(stack, context)
    assert context.memory[20:38] == bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x00, 0x00, 0x00])


def test_gasprice():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    blockchain_context = BlockchainContext(gas_price=69_000_000_000)
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data, blockchain_context=blockchain_context)

    evm_gasprice(stack, context)
    assert stack.pop() == 69_000_000_000


def test_extcodesize():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    ext_codes = defaultdict(partial(Code, b""))
    ext_codes[0xd707dadb71Abf7d978da36cc8379F2db8d0F8ebD] = bytes(i for i in range(256))
    ext_codes[0xe8538F3763DA91E6DB2B2DF6f52dFcB514b6660b] = bytes(0 for _ in range(394511))
    context = YulExecutionContext(storage, memory, call_data, code, return_data, ext_codes=ext_codes)

    stack.append(0xd707dadb71Abf7d978da36cc8379F2db8d0F8ebD)
    evm_extcodesize(stack, context)
    assert stack.pop() == 256

    stack.append(0xe8538F3763DA91E6DB2B2DF6f52dFcB514b6660b)
    evm_extcodesize(stack, context)
    assert stack.pop() == 394511

    stack.append(0x5B17238F57c61b2A0Dc7e7000DFdfe839F64C170)
    evm_extcodesize(stack, context)
    assert stack.pop() == 0


def test_extcodecopy():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(i for i in range(16))
    return_data = ReturnData([])
    stack: Stack = deque()
    ext_codes = defaultdict(partial(Code, b""))
    ext_codes[0xd707dadb71Abf7d978da36cc8379F2db8d0F8ebD] = bytes(0xFF - i for i in range(256))
    context = YulExecutionContext(storage, memory, call_data, code, return_data, ext_codes=ext_codes,
                                  self_address=0x44Eb29586b8D3c3f0b01eBbA0c85c71c6b306D3D)

    stack.append(18)
    stack.append(0)
    stack.append(0)
    stack.append(0x44Eb29586b8D3c3f0b01eBbA0c85c71c6b306D3D)
    evm_extcodecopy(stack, context)
    assert context.memory[0:18] == bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x00, 0x00])

    stack.append(18)
    stack.append(1)
    stack.append(20)
    stack.append(0x44Eb29586b8D3c3f0b01eBbA0c85c71c6b306D3D)
    evm_extcodecopy(stack, context)
    assert context.memory[20:38] == bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x00, 0x00, 0x00])

    stack.append(18)
    stack.append(0)
    stack.append(0)
    stack.append(0xd707dadb71Abf7d978da36cc8379F2db8d0F8ebD)
    evm_extcodecopy(stack, context)
    assert context.memory[0:18] == bytes([0xFF, 0xFE, 0xFD, 0xFC, 0xFB, 0xFA, 0xF9, 0xF8, 0xF7, 0xF6, 0xF5, 0xF4, 0xF3, 0xF2, 0xF1, 0xF0, 0xEF, 0xEE])


def test_returndatasize():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData(i for i in range(128))
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    evm_returndatasize(stack, context)
    assert stack.pop() == 128

    return_data = ReturnData(0 for _ in range(114088))
    context = YulExecutionContext(storage, memory, call_data, code, return_data)
    evm_returndatasize(stack, context)
    assert stack.pop() == 114088


def test_returndatacopy():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData(i for i in range(128))
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(18)
    stack.append(0)
    stack.append(0)
    evm_returndatacopy(stack, context)
    assert context.memory[0:18] == bytes(i for i in range(18))

    stack.append(32)
    stack.append(10)
    stack.append(20)
    evm_returndatacopy(stack, context)
    assert context.memory[20:52] == bytes(i + 10 for i in range(32))

    stack.append(32)
    stack.append(100)
    stack.append(20)
    with pytest.raises(EvmRevertError):
        evm_returndatacopy(stack, context)


def test_extcodehash():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(i for i in range(16))
    return_data = ReturnData([])
    stack: Stack = deque()
    ext_codes = defaultdict(partial(Code, b""))
    ext_codes[0xd707dadb71Abf7d978da36cc8379F2db8d0F8ebD] = bytes(0xFF - i for i in range(256))
    context = YulExecutionContext(storage, memory, call_data, code, return_data, ext_codes=ext_codes,
                                  self_address=0x44Eb29586b8D3c3f0b01eBbA0c85c71c6b306D3D)

    stack.append(0x965D319383560f6BF471a3555b50e314f00cD6fb)
    evm_extcodehash(stack, context)
    assert stack.pop() == 0

    h = Cryptodome.Hash.keccak.new(data=bytes(i for i in range(16)), digest_bits=256).digest()
    stack.append(0x44Eb29586b8D3c3f0b01eBbA0c85c71c6b306D3D)
    evm_extcodehash(stack, context)
    assert stack.pop() == int.from_bytes(h, "big", signed=False)

    h = Cryptodome.Hash.keccak.new(data=bytes(0xFF - i for i in range(256)), digest_bits=256).digest()
    stack.append(0xd707dadb71Abf7d978da36cc8379F2db8d0F8ebD)
    evm_extcodehash(stack, context)
    assert stack.pop() == int.from_bytes(h, "big", signed=False)


# TODO !!!
def test_blockhash():
    pass


def test_coinbase():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data,
                                  coinbase_address=0xfA8bafBEe41d6faB528AFc5d85040Bf378eeF1f2)

    evm_coinbase(stack, context)
    assert stack.pop() == 0xfA8bafBEe41d6faB528AFc5d85040Bf378eeF1f2


def test_timestamp():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    blockchain_context = BlockchainContext(timestamp=1646646394)
    context = YulExecutionContext(storage, memory, call_data, code, return_data, blockchain_context=blockchain_context)

    evm_timestamp(stack, context)
    assert stack.pop() == 1646646394


def test_number():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    blockchain_context = BlockchainContext(number=14338964)
    context = YulExecutionContext(storage, memory, call_data, code, return_data, blockchain_context=blockchain_context)

    evm_number(stack, context)
    assert stack.pop() == 14338964


def test_difficulty():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    blockchain_context = BlockchainContext(difficulty=11_916_661_372_945_950)
    context = YulExecutionContext(storage, memory, call_data, code, return_data, blockchain_context=blockchain_context)

    evm_difficulty(stack, context)
    assert stack.pop() == 11_916_661_372_945_950


def test_gaslimit():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    blockchain_context = BlockchainContext(gas_limit=30_058_590)
    context = YulExecutionContext(storage, memory, call_data, code, return_data, blockchain_context=blockchain_context)

    evm_gaslimit(stack, context)
    assert stack.pop() == 30_058_590


def test_chainid():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    blockchain_context = BlockchainContext(chain_id=ChainIdEnum.MORDOR)
    context = YulExecutionContext(storage, memory, call_data, code, return_data, blockchain_context=blockchain_context)

    evm_chainid(stack, context)
    assert stack.pop() == ChainIdEnum.MORDOR


def test_selfbalance():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    balances = defaultdict(int)
    balances[0xC9Cb15093AcE0be930f2d2981Fcdc0aACDabd4C5] = 151084
    context = YulExecutionContext(storage, memory, call_data, code, return_data, balances=balances,
                                  self_address=0xC9Cb15093AcE0be930f2d2981Fcdc0aACDabd4C5)

    evm_selfbalance(stack, context)
    assert stack.pop() == 151084


def test_basefee():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    blockchain_context = BlockchainContext(base_fee=26_485_513_913)
    context = YulExecutionContext(storage, memory, call_data, code, return_data, blockchain_context=blockchain_context)

    evm_basefee(stack, context)
    assert stack.pop() == 26_485_513_913


def test_pop():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(0x010203040506070809)
    evm_pop(stack, context)
    assert len(stack) == 0

    stack.append(10)
    stack.append(20)
    evm_pop(stack, context)
    assert len(stack) == 1
    assert stack.pop() == 10


def test_mload():
    storage: Storage = Storage()
    memory: Memory = Memory()
    memory[0:16] = bytes(i for i in range(16))
    memory[16:48] = bytes(chain([0] * 31, [0xFF]))
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(0)
    evm_mload(stack, context)
    assert stack.pop() == 0x000102030405060708090A0B0C0D0E0F00000000000000000000000000000000

    stack.append(1)
    evm_mload(stack, context)
    assert stack.pop() == 0x0102030405060708090A0B0C0D0E0F0000000000000000000000000000000000

    stack.append(10)
    evm_mload(stack, context)
    assert stack.pop() == 0x0A0B0C0D0E0F0000000000000000000000000000000000000000000000000000

    stack.append(16)
    evm_mload(stack, context)
    assert stack.pop() == 0xFF

    stack.append(17)
    evm_mload(stack, context)
    assert stack.pop() == 0xFF00


def test_mstore():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(0x000102030405060708090A0B0C0D0E0F)
    stack.append(0)
    evm_mstore(stack, context)
    assert context.memory[0:32] == bytes(chain([0] * 16, (i for i in range(16))))

    stack.append(0x000102030405060708090A0B0C0D0E0F)
    stack.append(18)
    evm_mstore(stack, context)
    assert context.memory[18:50] == bytes(chain([0] * 16, (i for i in range(16))))

    stack.append(0xFF)
    stack.append(0)
    evm_mstore(stack, context)
    assert context.memory[0:32] == bytes(chain([0] * 31, [0xFF]))

    stack.append(0xFF)
    stack.append(1)
    evm_mstore(stack, context)
    assert context.memory[0:33] == bytes(chain([0] * 32, [0xFF]))


def test_mstore8():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(0xEF)
    stack.append(1)
    evm_mstore8(stack, context)
    assert context.memory[0:32] == bytes(chain([0x00, 0xEF], [0] * 30))

    stack.append(0xBE)
    stack.append(0)
    evm_mstore8(stack, context)
    assert context.memory[0:32] == bytes(chain([0xBE, 0xEF], [0] * 30))


def test_sload():
    storage: Storage = Storage()
    storage[0xAABBCC] = 0x14482045
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(1)
    evm_sload(stack, context)
    assert stack.pop() == 0

    stack.append(0xAABBCC)
    evm_sload(stack, context)
    assert stack.pop() == 0x14482045


def test_sstore():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    stack.append(0x000102030405060708090A0B0C0D0E0F)
    stack.append(10)
    evm_sstore(stack, context)
    assert context.storage[10] == 0x000102030405060708090A0B0C0D0E0F

    stack.append(0xAABBCC)
    stack.append(10)
    evm_sstore(stack, context)
    assert context.storage[10] == 0xAABBCC

    context = YulExecutionContext(storage, memory, call_data, code, return_data,
                                  execution_context=ExecutionContextEnum.STATICCALL)
    stack.append(0xAABBCC)
    stack.append(10)
    with pytest.raises(EvmRevertError):
        evm_sstore(stack, context)


def test_jump():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code([0x60, 0x00, 0x5B])
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    context.pc = 0
    stack.append(2)
    evm_jump(stack, context)
    assert context.pc == 2

    stack.append(0)
    with pytest.raises(EvmRevertError):
        evm_jump(stack, context)


def test_jumpi():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code([0x60, 0x00, 0x5B])
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    context.pc = 0
    stack.append(0xFF)
    stack.append(2)
    evm_jumpi(stack, context)
    assert context.pc == 2

    context.pc = 0
    stack.append(0)
    stack.append(2)
    evm_jumpi(stack, context)
    assert context.pc == 1

    stack.append(0xFF)
    stack.append(0)
    with pytest.raises(EvmRevertError):
        evm_jumpi(stack, context)

    stack.append(0)
    stack.append(0)
    with pytest.raises(EvmRevertError):
        evm_jumpi(stack, context)


def test_pc():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    context.pc = 10245
    evm_pc(stack, context)
    assert stack.pop() == 10245
    assert context.pc == 10246


def test_msize():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    evm_msize(stack, context)
    assert stack.pop() == 0

    context.memory[0] = 0xFF
    evm_msize(stack, context)
    assert stack.pop() == 32

    _ = context.memory[64]
    evm_msize(stack, context)
    assert stack.pop() == 32 * 3


# TODO !!!
def test_gas():
    pass


def test_jumpdest():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code(b"")
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    context.pc = 1504
    evm_jumpdest(stack, context)
    assert context.pc == 1505
    assert len(stack) == 0


def test_push():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code([0x60, 0xAE, 0x61, 0x01, 0x02, 0x6F] + [i for i in range(16)] + [0x7F] + [i for i in range(32)])
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    context.pc = 0
    evm_push(stack, context)
    assert stack.pop() == 0xAE

    context.pc = 2
    evm_push(stack, context)
    assert stack.pop() == 0x0102

    context.pc = 5
    evm_push(stack, context)
    assert stack.pop() == 0x000102030405060708090A0B0C0D0E0F

    context.pc = 22
    evm_push(stack, context)
    assert stack.pop() == 0x000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F


def test_dup():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code([0x80, 0x81, 0x87, 0x8F])
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    context.pc = 0
    with pytest.raises(EvmRevertError):
        evm_dup(stack, context)

    context.pc = 0
    stack.append(0xAB)
    evm_dup(stack, context)
    assert stack.pop() == 0xAB
    assert stack.pop() == 0xAB
    assert len(stack) == 0

    context.pc = 1
    stack.append(0xAB)
    stack.append(0x01)
    evm_dup(stack, context)
    assert stack.pop() == 0xAB
    assert stack.pop() == 0x01
    assert stack.pop() == 0xAB

    context.pc = 2
    stack.append(0xAB)
    for i in range(7):
        stack.append(i)
    evm_dup(stack, context)
    assert stack.pop() == 0xAB
    for i in range(6, -1, -1):
        assert stack.pop() == i
    assert stack.pop() == 0xAB

    context.pc = 3
    stack.append(0xAB)
    for i in range(15):
        stack.append(i)
    evm_dup(stack, context)
    assert stack.pop() == 0xAB
    for i in range(14, -1, -1):
        assert stack.pop() == i
    assert stack.pop() == 0xAB


def test_swap():
    storage: Storage = Storage()
    memory: Memory = Memory()
    call_data: CallData = CallData(b"")
    code: Code = Code([0x90, 0x91, 0x94, 0x9F])
    return_data = ReturnData([])
    stack: Stack = deque()
    context = YulExecutionContext(storage, memory, call_data, code, return_data)

    context.pc = 0
    with pytest.raises(EvmRevertError):
        evm_swap(stack, context)

    context.pc = 0
    stack.append(0xAB)
    with pytest.raises(EvmRevertError):
        evm_swap(stack, context)
    stack.clear()

    context.pc = 0
    stack.append(0xAB)
    stack.append(0xCD)
    evm_swap(stack, context)
    assert stack.pop() == 0xAB
    assert stack.pop() == 0xCD
    assert len(stack) == 0
    stack.clear()

    context.pc = 1
    stack.append(0xAB)
    stack.append(0xCD)
    stack.append(0xEF)
    evm_swap(stack, context)
    assert stack.pop() == 0xAB
    assert stack.pop() == 0xCD
    assert stack.pop() == 0xEF
    stack.clear()

    context.pc = 2
    stack.append(0xAB)
    for i in range(4):
        stack.append(i)
    stack.append(0xCD)
    evm_swap(stack, context)
    assert stack.pop() == 0xAB
    for i in range(3, -1, -1):
        assert stack.pop() == i
    assert stack.pop() == 0xCD
    stack.clear()

    context.pc = 3
    stack.append(0xAB)
    for i in range(15):
        stack.append(i)
    stack.append(0xCD)
    evm_swap(stack, context)
    assert stack.pop() == 0xAB
    for i in range(14, -1, -1):
        assert stack.pop() == i
    assert stack.pop() == 0xCD
    stack.clear()

