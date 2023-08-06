import asyncio
import json

import socketio


class GSCNodeFunctionReceiverSocket:
    @classmethod
    async def create(cls, sio, gsdbs, oncnodefunction):
        self = GSCNodeFunctionReceiverSocket()
        self.gsdbs = gsdbs
        self.oncnodefunction = oncnodefunction
        self.sio = sio

        @self.sio.event
        async def connect():
            self._logger.info('connection established')

        @self.sio.event
        async def oncnodefunction(id, msg):
            self.oncnodefunction(id, msg)

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}&global=true')
        await self.sio.wait()

    def sendcnodefunctionResult(self, id, msg):
        self.sio.emit("answer", id, msg)


class GSCNodeFunctionReceiver:
    def __init__(self, gsdbs, oncnodefunction):
        self.sio = socketio.AsyncClient()
        self.gsdbs = gsdbs
        self.oncnodefunction = oncnodefunction

    def startSocket(self):
        asyncio.run(GSCNodeFunctionReceiverSocket.create(self.sio, self.gsdbs, self.oncnodefunction))

    def sendcnodefunctionanswer(self, id, msg):
        self.sio.emit("answer", {"id": id, "message": json.dumps(msg)})


class GSCNodeFunctionCallerSocket:
    @classmethod
    async def create(cls, gsdbs):
        self = GSCNodeFunctionReceiver()
        self.gsdbs = gsdbs

        @self.sio.event
        async def connect():
            self._logger.info('connection established')

        connectURL = ""

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}&caller=true')
        await self.sio.wait()


class GSCNodeFunctionCaller:
    def __init__(self, gsdbs, oncnodefunction):
        self.sio = socketio.AsyncClient()
        self.gsdbs = gsdbs
        self.oncnodefunction = oncnodefunction

    def startSocket(self):
        asyncio.run(GSCNodeFunctionReceiverSocket.create(self.sio, self.gsdbs, self.oncnodefunction))

    def sendcnodefunction(self, target, msg):
        self.sio.emit("oncnodefunction", {"target": target, "message": json.dumps(msg)})


receiver = None


def oncnodefunction(id, msg):
    print(f'id:{str(id)},msg:{str(msg)}')
    receiver.sendcnodefunctionanswer(id, msg)


if __name__ == '__main__':
    receiver = GSCNodeFunctionReceiver(None, oncnodefunction)
    receiver.startReceiver()
