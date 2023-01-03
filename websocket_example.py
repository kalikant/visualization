import asyncio
import json
import numpy as np
import websockets


class Grid:
    def __init__(self, name, usedProcess, pendingProcess, remainingProcess):
        self.name = name
        self.usedProcess = usedProcess
        self.pendingProcess = pendingProcess
        self.remainingProcess = remainingProcess


def get_data():
    grids = []

    grids.append(Grid('G1', np.random.randint(10, 55), np.random.randint(1, 5), np.random.randint(5, 40)))
    grids.append(Grid('G2', np.random.randint(10, 65), np.random.randint(1, 10), np.random.randint(5, 25)))
    grids.append(Grid('G3', np.random.randint(10, 75), np.random.randint(1, 5), np.random.randint(5, 20)))
    grids.append(Grid('G4', np.random.randint(10, 85), np.random.randint(1, 5), np.random.randint(5, 10)))
    grids.append(Grid('G5', np.random.randint(10, 35), np.random.randint(1, 15), np.random.randint(5, 50)))

    return grids

data = get_data()

async def emit_data(websocket, path):
    global data
    while True:
        if len(data) > 0:
            # send the data to the web page
            obj = data.pop()
            await websocket.send(json.dumps(obj.__dict__))

            # wait for a specified amount of time before sending more data
            await asyncio.sleep(1)
        else:
            data = get_data()


# start the server
start_server = websockets.serve(emit_data, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
