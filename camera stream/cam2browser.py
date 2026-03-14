import cv2
import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, VideoStreamTrack, RTCSessionDescription
from av import VideoFrame

pcs = set()


class CameraTrack(VideoStreamTrack):

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    async def recv(self):

        pts, time_base = await self.next_timestamp()

        ret, frame = self.cap.read()

        if not ret:
            await asyncio.sleep(0.01)
            return await self.recv()

        frame = VideoFrame.from_ndarray(frame, format="bgr24")

        frame.pts = pts
        frame.time_base = time_base

        return frame


async def offer(request):

    params = await request.json()

    pc = RTCPeerConnection()

    pc.addTrack(CameraTrack())   # IMPORTANT: add track before remote description

    offer = RTCSessionDescription(
        sdp=params["sdp"],
        type=params["type"]
    )

    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    })

async def index(request):
    return web.FileResponse("index.html")

app = web.Application()
app.router.add_get("/", index)
app.router.add_post("/offer", offer)

web.run_app(app, port=8080)