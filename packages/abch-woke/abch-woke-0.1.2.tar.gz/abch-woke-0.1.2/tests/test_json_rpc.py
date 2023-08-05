from woke.json_rpc import JsonRpcCommunicator


async def test_anvil():
    communicator = JsonRpcCommunicator()
    print(await communicator.eth_block_number())
