import logging
from concurrent import futures

import grpc
import torch
from lib.ml_predictions_pb2 import *
from lib.ml_predictions_pb2_grpc import MlPredictionsServicer, add_MlPredictionsServicer_to_server
from lib.utils import *
from PIL import Image as I

logger = logging.getLogger(__name__)


class PredictionServicer(MlPredictionsServicer):

    def __init__(self):

        self.__load_model()


    def __load_model(self, model="yolov5m"):

        self.model = torch.hub.load("ultralytics/yolov5", model, pretrained=True)
        self.model.eval()


    def __predict_one(self, request):

        img = convert_image_proto(request)

        results = torch_pred_to_json(self.model([img]))

        frame = request.frame

        return PredictionCollection(object=to_protobuf_prediction(results), frame=frame)

    def PredictSingleImage(self, request, context):

        logger.info("Predicting single image...")

        return self.__predict_one(request)

    def PredictMultipleImages(self, request_iterator, context):

        logger.info("Predicting multiple frames/images...")

        for req in request_iterator:

            logger.info(f"[RECEIVED FROM STREAM] frame {req.frame}")

            yield self.__predict_one(req)

        logger.info("End of predictions.")



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MlPredictionsServicer_to_server(PredictionServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info("Server started...")
    server.wait_for_termination()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    serve()
