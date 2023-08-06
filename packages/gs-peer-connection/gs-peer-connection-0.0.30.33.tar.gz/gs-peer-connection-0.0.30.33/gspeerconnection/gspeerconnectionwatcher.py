import ast
import json
import logging

import socketio
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCIceServer, RTCConfiguration
from aiortc.contrib.media import MediaRelay, MediaBlackhole
from aiortc.rtcrtpreceiver import RemoteStreamTrack

relay = MediaRelay()


class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, gsdbs, source, onframe):
        super().__init__()
        self.track = track
        self.onframe = onframe
        self.source = source
        self.gsdbs = gsdbs

    async def recv(self):
        frame = await self.track.recv()
        await self.onframe(self.gsdbs, self.source, frame)
        return frame


class GSPeerConnectionWatcher:

    @classmethod
    async def create(cls, gsdbs, target, onframe=None, onmessage=None, ontrack=None, ontrackended=None):
        self = GSPeerConnectionWatcher()
        self.rtconfiList = []
        self.sio = socketio.AsyncClient()
        self.gsdbs = gsdbs
        self.onframe = onframe
        self.target = target
        self.onmessage = onmessage
        self.ontrack = ontrack
        self.ontrackended = ontrackended
        self.logger = logging.getLogger(__name__)

        if self.gsdbs.credentials["stunenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["stunserver"]))
        if self.gsdbs.credentials["turnenable"]:
            self.rtconfiList.append(RTCIceServer(self.gsdbs.credentials["turnserver"],
                                                 self.gsdbs.credentials["turnuser"],
                                                 self.gsdbs.credentials["turnpw"]))

        @self.sio.event
        async def connect():
            self.logger.info('connection established')

        @self.sio.event
        async def joined(id):
            self.logger.info("joined")

        @self.sio.event
        async def broadcaster(id):
            if len(self.rtconfiList) > 0:
                self.peerConnections = RTCPeerConnection(configuration=RTCConfiguration(self.rtconfiList))
            else:
                self.peerConnections = RTCPeerConnection()

            self.peerConnections.addTransceiver('video', direction='recvonly')

            @self.peerConnections.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                if self.peerConnections.iceConnectionState == "complete":
                    pass

                if self.peerConnections.iceConnectionState == "failed":
                    await self.peerConnections.close()

            @self.peerConnections.on("track")
            async def on_track(track):
                if track.kind == "video":
                    if self.ontrack is not None:
                        self.logger.info("on track received.Recording started")
                        await self.ontrack(self.gsdbs, track, self.target)
                    if self.onframe is not None:
                        self.logger.info("on track received. onframe started")
                        blackHole = MediaBlackhole()
                        mediaTrack = VideoTransformTrack(relay.subscribe(track), self.gsdbs, self.target, self.onframe)
                        blackHole.addTrack(mediaTrack)
                        await blackHole.start()

                # @track.on("ended")
                # async def on_ended():
                #     await self.ontrackended(self.gsdbs, self.target)

            await self.peerConnections.setLocalDescription(await self.peerConnections.createOffer())
            await self.sio.emit("watcher",
                                {"target": self.target,
                                 "sdp": {"type": self.peerConnections.localDescription.type,
                                         "sdp": self.peerConnections.localDescription.sdp}})

        @self.sio.event
        async def answer(id, description):
            if isinstance(description, dict):
                desc = type('new_dict', (object,), description)
            else:
                desc = type('new_dict', (object,), ast.literal_eval(description))
            await self.peerConnections.setRemoteDescription(desc)

        @self.sio.event
        async def disconnectBroadcaster(id, target):
            await self.ontrackended(self.gsdbs, target)

        if "localhost" in self.gsdbs.credentials["signalserver"]:
            connectURL = f'{self.gsdbs.credentials["signalserver"]}:{str(self.gsdbs.credentials["signalport"])}'
        else:
            connectURL = self.gsdbs.credentials["signalserver"]

        await self.sio.connect(
            f'{connectURL}?gssession={self.gsdbs.cookiejar.get("session")}.{self.gsdbs.cookiejar.get("signature")}{self.gsdbs.credentials["cnode"]}&target={self.target}')
        await self.sio.wait()
