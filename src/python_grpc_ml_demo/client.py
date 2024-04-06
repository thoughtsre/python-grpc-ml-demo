from PIL import Image as I
import grpc
import cv2
import gradio as gr

from lib.ml_predictions_pb2_grpc import MlPredictionsStub
from lib.ml_predictions_pb2 import Image
from lib.utils import *


def run(stub):
    
    demo = gr.Interface(fn=lambda x: x, inputs = ["text"], outputs = ["text"])
    
    demo.launch()
        

if __name__ == "__main__":
    
    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = MlPredictionsStub(channel)
        
        run(stub)
        # img = I.open("assets/cat_dog.jpg")
        # print(img)
        
        # img_proto = pil_to_proto(img)
        
        # res = stub.PredictSingleImage(img_proto)
        
        # print(res)
        
        # vid_frame_stream = video_stream("assets/KFC.mp4")
        
        # resp = stub.PredictMultipleImages(proto_stream(vid_frame_stream))
        
        # for r in resp:
            
        #     print(r)
            