from typing import Iterator, Optional

import cv2
import gradio as gr
from PIL import Image as I

from .ml_predictions_pb2_grpc import MlPredictionsStub
from .utils import *


class ImageModule:

    def __init__(self, stub: MlPredictionsStub):
        """Class for image prediction function of demo.

        Detects objects in a single image.

        """

        self.input_image = gr.Image(
            type="pil", sources=["upload"], show_label=False, show_share_button=False, show_download_button=False
        )
        self.output_image = gr.Image(type="pil", show_label=False, show_share_button=False, show_download_button=False)
        self.stub = stub


    def predict(self, image: I) -> I:

        result = self.stub.PredictSingleImage(pil_to_proto(image))

        return draw_annotations(image, result.object)

    def interface(self) -> gr.Interface:
        """Returns Gradio interface for single image prediction"""

        return gr.Interface(self.predict, title="Image", inputs=[self.input_image], outputs=[self.output_image])


class VideoModule:

    def __init__(self, stub: MlPredictionsStub, predict_every: int = 24):
        """Class for video prediction function of demo.

        Detects objects in selected frames in a video.

        """

        self.stub = stub
        self.predict_every = predict_every
        self.frames = {}

        self.input_image = gr.Video(
            sources=["upload"], show_label=False, show_share_button=False, show_download_button=False
        )

        self.output_image = gr.Gallery(
            type="pil", columns=3, show_label=False, show_share_button=False, show_download_button=False
        )


    def video_stream(
        self,
        filepath: str,
        max_size: tuple[int, int] = (960, 540),
        yield_every: int = 5,
        max_frames: Optional[int] = None,
    ) -> Iterator[tuple[int, I.Image]]:
        """Creates a generator of video frames

        Parameters
        ----------
        filepath: str
            Path to video

        max_size: tuple[int, int]
            Maximum size (in pixels) of each frame. Will resize to the max_size.

            This is also because there is a default max message size to gRPC.

        yield_every: int
            Yield every n frames. Set to 1 if prediction in every frame is neecded.

            Default: 5

        max_frames: int
            Predict up to max_frames.
        """

        vid = cv2.VideoCapture(filepath)

        assert vid.isOpened(), "Video file not found!"

        cur_frame = 0

        while True:

            ret, f = vid.read()

            cur_frame += 1

            if (not ret) or (max_frames and (cur_frame >= max_frames)):

                break

            if (cur_frame % yield_every) == 0:

                cur_frame_im = frame_to_pil(f).resize(max_size)

                self.frames[cur_frame] = cur_frame_im

                yield cur_frame, cur_frame_im

        vid.release()

        return

    def predict(self, video_path):

        vid_frame_stream = self.video_stream(video_path, yield_every=self.predict_every)

        resp = self.stub.PredictMultipleImages(proto_stream(vid_frame_stream))

        all_preds = []

        for res in resp:

            image = self.frames[res.frame]

            all_preds.append(draw_annotations(image, res.object))

            del self.frames[res.frame]

        return all_preds

    def interface(self):

        return gr.Interface(self.predict, title="Video", inputs=[self.input_image], outputs=[self.output_image])
