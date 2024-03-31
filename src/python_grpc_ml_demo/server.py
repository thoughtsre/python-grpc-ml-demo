import torch
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image

import grpc

from lib.protos.ml_predictions_pb2_grpc import MlPredictionsServicer
from lib.protos.ml_predictions_pb2 import *

def convert_image_proto(image_proto): 
    Image.frombytes(image_proto.mode, 
                    (image_proto.width, image_proto.height),
                    image_proto.data)

class PredictionServicer(MlPredictionsServicer): 
    
    def __init__(self):
        
        self.wts = ResNet18_Weights.IMAGENET1K_V1
        self,model = resnet18(weights=self.wts)
        self,model.eval()
        self.preprocess = self.wts.transforms()
        self.categories = self.wts.meta["categories"]
        
        return
    
    def PredictSingleImage(self, request, context):
        
        img = convert_image_proto(request)
        img_transformed = self.preprocess(img).unsqueeze()
        
        if len(img_transformed.size) != 4:
            
            context.abort_with_status(grpc.StatusCode.ABORTED)
            
        pred = self.model(img_transformed)
        class_id = pred.argmax().item()
        
        return Prediction(prediction = self.categories[class_id])