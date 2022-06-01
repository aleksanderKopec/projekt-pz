import asyncio
import base64
import websockets
import json
import requests

HOSTED_DOMAIN = "chatapp.westeurope.cloudapp.azure.com"

API_URL = f"http://{HOSTED_DOMAIN}:8000/api"
WS_URL = f"ws://{HOSTED_DOMAIN}:8000/ws"

TEST_ROOM_NAME = f"{'test'*50}"

TEST_ROOM = base64.b64encode(TEST_ROOM_NAME.encode('ascii')).decode('ascii')
TEST_USERNAME = "test_user"

SAMPLE_MESSAGE_LIST = [
    {
        "message": "test message 1",
        "is_image": False
    },
    {
        "message": "test message 2",
    },
    {
        "message": "test message 3",
        "is_image": False
    },
    {
        "message": "test message 4",
    },
    {
        "message": "test message 5",
        "is_image": False
    },
]


class Result:
    result_pos = 0

    def __init__(self, succeeded: bool, reason: str = ""):
        self.succeeded = succeeded
        self.reason = reason

        if succeeded:
            Result.result_pos += 1


async def exchange_messages() -> Result:
    try:
        async with websockets.connect(f"{WS_URL}/{TEST_ROOM}?username={TEST_USERNAME}") as websocket:
            for message in SAMPLE_MESSAGE_LIST:
                await websocket.send(json.dumps(message))
                received_message = await websocket.recv()
                assert json.loads(received_message)["message"] == message["message"], \
                    "Received message doesn't match with sent one."
    except Exception as e:
        return Result(False, e)
    return Result(True)


async def get_messages() -> Result:
    try:
        url = f"{API_URL}/{TEST_ROOM}"
        response = requests.get(url).json()
        for i in range(len(SAMPLE_MESSAGE_LIST)):
            sample_message = SAMPLE_MESSAGE_LIST[len(SAMPLE_MESSAGE_LIST)-i-1]["message"]
            assert response["messages"][i]["message"] == sample_message, \
                f'Received message {response["messages"][i]["message"]} does not match sent {sample_message}'
    except Exception as e:
        return Result(False, e)
    return Result(True)


async def main():
    tests = [
        exchange_messages,
        get_messages,
    ]
    for test in tests:
        result = await test()
        print(
            f"Test {'succeeded' if result.succeeded else 'failed'}, {result.reason}")

    print(f"Tests passed: {Result.result_pos}/{len(tests)}")


if __name__ == "__main__":
    asyncio.run(main())
