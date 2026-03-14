import cv2
import asyncio
from aiortc import RTCPeerConnection
from aiortc.contrib.media import MediaBlackhole

pc = RTCPeerConnection()

@pc.on("track")
async def on_track(track):

    print("Track received:", track.kind)

    if track.kind == "video":

        while True:
            frame = await track.recv()

            img = frame.to_ndarray(format="bgr24")

            cv2.imshow("WebRTC Stream", img)

            if cv2.waitKey(1) == 27:
                break


async def run():

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

asyncio.run(run())