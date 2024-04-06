from PIL import Image as I
import grpc
import cv2
import gradio as gr

from lib.ml_predictions_pb2_grpc import MlPredictionsStub
from lib.ml_predictions_pb2 import Image
from lib.utils import *


# def pil_to_proto(img: I) -> Image:
    
#     (i_width, i_height) = img.size
    
#     return Image(mode=img.mode,
#                  width=i_width,
#                  height=i_height,
#                  data=img.tobytes()
#                  )
    
# def frame_to_pil(frame) -> I:
    
#     return I.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# def video_stream(filepath, size=(960, 540), yield_every=5, max_frames=None):
    
#     vid = cv2.VideoCapture(filepath)
    
#     assert vid.isOpened(), "Video file not found!"
    
#     cur_frame = 0
    
#     while True:
        
#         ret, f = vid.read()
        
#         cur_frame += 1
        
#         if (not ret) or (max_frames and (cur_frame >= max_frames)):
            
#             break
        
#         if yield_every & ((cur_frame % yield_every) == 0):
            
#             yield frame_to_pil(f).resize(size)
            
#     vid.release()
    
#     return

# def proto_stream(frame_stream):
    
#     for f in frame_stream:
        
#         yield pil_to_proto(f)

def run(stub):
    
    demo = gr.Interface(fn=lambda x: x, inputs = ["text"], outputs = ["text"])
    
    demo.launch()
        

if __name__ == "__main__":
    
    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = MlPredictionsStub(channel)
        
        # run(stub)
        img = I.open("assets/cat_dog.jpg")
        print(img)
        
        img_proto = pil_to_proto(img)
        
        res = stub.PredictSingleImage(img_proto)
        
        print(res)
        
        vid_frame_stream = video_stream("assets/KFC.mp4")
        
        resp = stub.PredictMultipleImages(proto_stream(vid_frame_stream))
        
        for r in resp:
            
            print(r)
            