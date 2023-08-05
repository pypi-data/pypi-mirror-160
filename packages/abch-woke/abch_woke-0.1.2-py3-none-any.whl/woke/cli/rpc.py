import asyncio

import click

from woke.json_rpc import JsonRpcCommunicator


async def connect():
    communicator = JsonRpcCommunicator()
    print(await communicator.eth_block_number())


@click.command(name="rpc")
def run_rpc():
    asyncio.run(connect())
