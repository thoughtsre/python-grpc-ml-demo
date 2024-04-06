import logging
import torch
from PIL import Image as I
import grpc
from concurrent import futures

from lib.ml_predictions_pb2_grpc import MlPredictionsServicer, add_MlPredictionsServicer_to_server
from lib.ml_predictions_pb2 import *
from lib.utils import *
    
logger = logging.getLogger(__name__)
    

class PredictionServicer(MlPredictionsServicer): 
    
    def __init__(self):
        
        self.__load_model()
        
        return
    
    def __load_model(self, model="yolov5s"):
        
        self.model = torch.hub.load('ultralytics/yolov5', model, pretrained=True)
        self.model.eval()
        
        return
    
    def __predict_one(self, request):
        
        img = convert_image_proto(request)
        
        results = torch_pred_to_json(self.model([img]))
        
        return PredictionCollection(object = to_protobuf_prediction(results))
        
    def PredictSingleImage(self, request, context):
        
        logger.info("Predicting single image...")
        
        return self.__predict_one(request)
        
    
    def PredictMultipleImages(self, request_iterator, context):
        
        logger.info("Predicting multiple frames/images...")
        
        for i, req in enumerate(request_iterator):
            
            logger.info(f"... frame {i+1}")
            
            yield self.__predict_one(req)
            
        logger.info(f"End of predictions.")
        
        return
            
            

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MlPredictionsServicer_to_server(
        PredictionServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info("Server started...")
    server.wait_for_termination()


if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    serve()