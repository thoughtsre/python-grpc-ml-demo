import logging
import gradio as gr
import grpc

from lib.ml_predictions_pb2_grpc import MlPredictionsStub
from lib.modules import *
from lib.utils import *

logging.basicConfig(level=logging.WARN)


def run(stub):

    IM = ImageModule(stub)
    VM = VideoModule(stub)

    image_interface = IM.interface()
    video_interface = VM.interface()

    demo = gr.TabbedInterface(
        [image_interface, video_interface], ["Image", "Video"], title="ML Predictions with gRPC in Python"
    )

    demo.launch(inbrowser=True, debug=True)


if __name__ == "__main__":

    with grpc.insecure_channel("localhost:50051") as channel:

        stub = MlPredictionsStub(channel)

        run(stub)
