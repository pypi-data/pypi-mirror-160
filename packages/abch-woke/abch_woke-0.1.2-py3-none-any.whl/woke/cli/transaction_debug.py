import asyncio
import sys
from pathlib import Path
from typing import Dict, Tuple

import aiohttp
import click
from click import Context

from woke.build_artifacts_parser import BrownieContractArtifacts, load_brownie_artifacts
from woke.debugger.decoders import decode
from woke.debugger.resolver import Resolver
from woke.json_rpc import JsonRpcCommunicator

from .console import console


@click.command(name="debug")
@click.option("--port", default=8545, type=int, help="Port of the JSON RPC HTTP server.")
@click.pass_context
def run_transaction_debug(ctx: Context, port: int) -> None:
    asyncio.run(runner(port))


async def runner(port: int) -> None:
    artifacts = load_brownie_artifacts()
    r = Resolver(artifacts)
    r.setup()
    codes = set()
    init_codes = set()

    deployed_contracts: Dict[int, BrownieContractArtifacts] = {}  # address -> contract info

    async with aiohttp.ClientSession() as session:
        rpc_communicator = JsonRpcCommunicator(port=port, client_session=session)
        block_number = await rpc_communicator.eth_block_number()

        for block_no in range(block_number):
            block = await rpc_communicator.eth_get_block_by_number(block_no, True)
            if block.transactions:
                for transaction in block.transactions:
                    if transaction.to_addr is None:
                        init_code = transaction.input
                        init_codes.add(init_code)
                        receipt = await rpc_communicator.eth_get_transaction_receipt(transaction.hash)
                        deployed_code = await rpc_communicator.eth_get_code(receipt.contract_address, "latest")
                        codes.add(deployed_code)

                        contract = None

                        for artifact in artifacts:
                            if artifact.bytecode == init_code[2:]:
                                contract = artifact
                                break
                        if contract is None:
                            # TODO this does not work
                            for artifact in artifacts:
                                if artifact.deployed_bytecode == deployed_code[2:]:
                                    contract = artifact
                                    break

                        if contract is None:
                            print("Unable to detect deployed contract in following transaction:")
                            console.print_json(transaction.json())
                        else:
                            deployed_contracts[int(receipt.contract_address, 0)] = contract
                            storage = await rpc_communicator.eth_get_storage_at(receipt.contract_address, 0, "latest")
                            console.print(f"Deployed contract {contract.contract_name} at address {receipt.contract_address}")
                            print(f"storage: {storage}")
                        print("=========================================================")
                    else:
                        # determine function being called
                        to_address = int(transaction.to_addr, 0)
                        brownie_artifact = deployed_contracts[to_address]
                        method_identifier = transaction.input[2:10]
                        input = bytes.fromhex(transaction.input[2:])

                        function = r.resolve_function(method_identifier)
                        arguments = []
                        input_offset = 4
                        for argument in function.parameters.parameters:
                            arguments.append(decode(input[input_offset : input_offset + 32], argument))
                            input_offset += 32

                        if function is None:
                            print("Unable to detect function being called in following transaction:")
                            console.print_json(transaction.json())
                        else:
                            args = ", ".join(str(x) for x in arguments)
                            console.print(f"Called {brownie_artifact.contract_name}.{function.name}({args})")
                        print("=========================================================")
