from ..sdk import *

def ReadPcap(path: str, frameMode: int = 0):
    capture_path = path 
    # Initialize
    Initialize()
    # LoadPcap
    # speed=100 means 1x speed. Speed=0 means as fast as possible.
    LoadPcap(capture_path, speed=0)
    # Enable FIFO feature
    # Frame aggregation mode set to 0(natrual). Allocate 400 frame buffers in the frame FIFO
    EnableFrameFifo(frameMode=frameMode, nFrames=400)

    # Loop until pcap replay is finished
    while not ReplayIsFinished() or not FrameFifoEmpty():
        frame = FrameFifoGetFrame(timeout=2000) # 2000 ms

        if not frame is None:
            yield frame
            FrameFifoRelease()

    # Disable FIFO feature
    DisableFrameFifo()
    # Deinitialize
    Deinitialize()
