from PIL import Image as I
import grpc
import cv2

from lib.ml_predictions_pb2_grpc import MlPredictionsStub
from lib.ml_predictions_pb2 import Image


def pil_to_proto(img: I) -> Image:
    
    (i_width, i_height) = img.size
    
    return Image(mode=img.mode,
                 width=i_width,
                 height=i_height,
                 data=img.tobytes()
                 )
    
def frame_to_pil(frame) -> I:
    
    return I.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

def video_stream(filepath: str, yield_every=5, max_frames=None):
    
    vid = cv2.VideoCapture(filepath)
    
    assert vid.isOpened(), "Video file not found!"
    
    cur_frame = 0
    
    while True:
        
        ret, f = vid.read()
        
        cur_frame += 1
        
        if (not ret) or (cur_frame >= max_frames):
            
            break
        
        if yield_every & ((cur_frame % yield_every) == 0):
            
            yield frame_to_pil(f)
            
    vid.release()
    
    return
        

if __name__ == "__main__":
    
    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = MlPredictionsStub(channel)
        
        img = I.open("assets/cat_dog.jpg")
        
        img_proto = pil_to_proto(img)
        
        res = stub.PredictSingleImage(img_proto)
        
        print(res)
        
        vid_frame_stream = video_stream("assets/KFC.mp4")
        
        for r in stub.PredictMultipleImages(vid_frame_stream):
            
            print(r)
        