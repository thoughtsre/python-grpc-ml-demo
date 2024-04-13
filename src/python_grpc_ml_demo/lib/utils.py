import logging
from typing import Dict, List

import cv2
from google.protobuf.message import Message
from lib.ml_predictions_pb2 import *
from PIL import Image as I
from PIL import ImageDraw, ImageFont


def convert_image_proto(image_proto: Message) -> I.Image:
    """Converts an Image protobuf message to Pillow Image"""
    return I.frombytes(image_proto.mode, (image_proto.width, image_proto.height), image_proto.data)


def to_protobuf_prediction(predictions: List[Dict]) -> List[Message]:
    """Converts list of dictionary containing predictions to list of Prediction protobuf messages"""

    return [
        Prediction(xmin=r["xmin"], ymin=r["ymin"], xmax=r["xmax"], ymax=r["ymax"], name=r["name"]) for r in predictions
    ]


def torch_pred_to_json(pred) -> List[Dict]:
    """Convert model prediction to list of dictionaries"""

    return pred.pandas().xyxy[0].to_dict(orient="records")


def pil_to_proto(img: I, frame: int = 0) -> I:
    """Convert PIL image into Image protobuf"""

    (i_width, i_height) = img.size

    return Image(mode=img.mode, width=i_width, height=i_height, data=img.tobytes(), frame=frame)


def frame_to_pil(frame) -> I.Image:
    """Convert OpenCV frame into Pillow Image"""

    return I.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


def proto_stream(frame_stream):
    """Generator for stream of video frames"""

    for i, f in frame_stream:

        yield pil_to_proto(f, frame=i)


def draw_annotations(image: I, results: List[Message]) -> I.Image:
    """Draw annotations on image given list of predictions"""

    annotated_img = ImageDraw.Draw(image)

    for res in results:

        # logging.info(f"xmin: {res.xmin}, xmax: {res.xmax}, ymin: {res.ymin}, ymax: {res.ymax}")

        scale = int(res.xmax - res.xmin)
        font = ImageFont.load_default(size=max(10, scale / 10))
        annotated_img.rectangle(
            [(res.xmin, res.ymin), (res.xmax, res.ymax)], outline="green", width=max(2, int(scale / 100))
        )
        annotated_img.text((res.xmin, res.ymin), res.name, fill="green", font=font)

    return image
