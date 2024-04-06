import cv2
from PIL import Image as I

from lib.ml_predictions_pb2 import *


def convert_image_proto(image_proto): 
    return I.frombytes(image_proto.mode, 
                       (image_proto.width, image_proto.height),
                       image_proto.data)
    
def to_protobuf_prediction(predictions):
    
    return [Prediction(
        xmin = _["xmin"],
        ymin = _["ymin"],
        xmax = _["xmax"],
        ymax = _["ymax"],
        name = _["name"]) for _ in predictions]
    
def torch_pred_to_json(pred):
    
    return pred.pandas().xyxy[0].to_dict(orient="records")

def pil_to_proto(img: I) -> Image:
    
    (i_width, i_height) = img.size
    
    return Image(mode=img.mode,
                 width=i_width,
                 height=i_height,
                 data=img.tobytes()
                 )
    
def frame_to_pil(frame) -> I:
    
    return I.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

def video_stream(filepath, size=(960, 540), yield_every=5, max_frames=None):
    
    vid = cv2.VideoCapture(filepath)
    
    assert vid.isOpened(), "Video file not found!"
    
    cur_frame = 0
    
    while True:
        
        ret, f = vid.read()
        
        cur_frame += 1
        
        if (not ret) or (max_frames and (cur_frame >= max_frames)):
            
            break
        
        if yield_every & ((cur_frame % yield_every) == 0):
            
            yield frame_to_pil(f).resize(size)
            
    vid.release()
    
    return

def proto_stream(frame_stream):
    
    for f in frame_stream:
        
        yield pil_to_proto(f)