import logging
import time

import cv2
import sys


class GSHLSPlayer:

    @classmethod
    async def create(cls, gsdbs, url, onframe):
        self = GSHLSPlayer()
        self.gsdbs = gsdbs
        self.url = url
        self.onframe = onframe
        self._logger = logging.getLogger(__name__)
        self.url += f"&vision=true&session={self.gsdbs.cookiejar.get('session')}&signature={self.gsdbs.cookiejar.get('signature')}"
        cap = cv2.VideoCapture(self.url)

        if cap.isOpened() == False:
            self._logger.error("unable to open playlist")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            onframe(self.gsdbs, "hls_playlist", frame)
        cap.release()
        cv2.destroyAllWindows()