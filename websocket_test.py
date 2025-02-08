import asyncio
import websockets
import json

from datetime import datetime


async def send_time(websocket):
    pass
    # while True:
    #     print(f"send_time sleeping for {datetime.now()}")
    #     await asyncio.sleep(30)
    #     print(f"send_time OK for {datetime.now()}")

    # await websocket.send(json_data)
    # print(f"(client) send to server: {json_data}")

async def receive_message(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(f"(client) recv from server: {message}")
        except websockets.ConnectionClosed:
            print("Connection with server closed")
            break


async def hello(uri):
    async with websockets.connect(uri) as websocket:

        current_time = datetime.now().strftime('%H:%M:%S')
        datas = {
            'action': 'login',
            'data': {
                'time': current_time,
                'ident_id': 'benny123'
            }
        }
        json_data = json.dumps(datas)
        await websocket.send(json_data)
        print(f"(client) send to server: {current_time}")

        # send_task = asyncio.create_task(send_time(websocket))
        receive_task = asyncio.create_task(receive_message(websocket))

        # 等待 10 分钟（600 秒），然后取消任务
        await asyncio.sleep(60 * 3)


        # send_task.cancel()
        receive_task.cancel()

        try:
            await websocket.close()
        except Exception as e:
            print(f"Error closing connection: {e}")


asyncio.get_event_loop().run_until_complete(hello('ws://localhost:2021'))
