import asyncio
import logging
from typing import List

import aiohttp
import click as click
import pydantic
from pydantic.main import BaseModel

from woke.config import WokeConfig
from woke.json_rpc import JsonRpcCommunicator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _to_camel(s: str) -> str:
    split = s.split("_")
    return split[0].lower() + "".join([w.capitalize() for w in split[1:]])


class EtherscanModel(BaseModel):
    class Config:
        alias_generator = _to_camel
        allow_population_by_field_name = True
        extra = pydantic.Extra.ignore


class Tx(EtherscanModel):
    block_number: int
    time_stamp: int
    from_: str
    to: str
    value: int
    contract_address: str
    input: str
    type: str
    gas: int
    gas_used: int
    is_error: bool
    err_code: str


class Response(EtherscanModel):
    status: str
    message: str
    result: List[Tx]


async def debug_trace(tx: str, api_key: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.etherscan.io/api?module=proxy&action=debug_traceTransaction&txhash={tx}&apikey={api_key}") as resp:
            data = await resp.json()
            return data


async def source_code(account: str, api_key: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={account}&apikey={api_key}") as resp:
            data = await resp.json()
            return data


async def etherscan_get_transactions(tx: str, api_key: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={tx}&apikey={api_key}") as resp:
            data = await resp.json()
            return data


@click.command(name="tx")
@click.argument("transaction", type=str)
@click.pass_context
def run_transaction(
        ctx: click.Context, transaction: str = "0x78658194517db60eb8887b3ca47f20b9867bbe3012358e4cf29a958479175ae1"
) -> None:
    config = WokeConfig()
    config.load_configs()
    logger.debug(config.api_keys.etherscan)
    asyncio.run(run(transaction, config))


async def run(tx: str, config: WokeConfig) -> None:
    api_key = config.api_keys.etherscan

    async with aiohttp.ClientSession() as session:
        json_rpc = JsonRpcCommunicator(f"https://weathered-broken-surf.discover.quiknode.pro/{config.api_keys.quicknode}", client_session=session)
        trace_info = await json_rpc.debug_trace_transaction(tx)
        logger.info(trace_info)

    info = await etherscan_get_transactions(tx, api_key)
    logger.debug(info["result"]["to"])
    logger.debug(await source_code(info["result"]["to"], api_key))
    #logger.debug(await debug_trace(tx, api_key))
