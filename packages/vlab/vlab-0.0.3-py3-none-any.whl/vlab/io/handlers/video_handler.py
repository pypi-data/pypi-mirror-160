import os

import cv2

from vlab.io.handlers.base import BaseFileHandler


class VideoReader:
    """
    Video class with similar usage to a list object.
    """

    def __init__(self, filepath, to_rgb=True):
        self.filepath = filepath
        self.cap = cv2.VideoCapture(filepath)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.to_rgb = to_rgb

    def __len__(self):
        return self.frame_count

    def __getitem__(self, index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = self.cap.read()
        if not ret:
            raise IndexError("Video index out of range")
        if self.to_rgb:
            if frame.shape[-1] == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif frame.shape[-1] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
        return frame

    def __iter__(self):
        for i in range(self.frame_count):
            yield self[i]

    def __repr__(self):
        return f"VideoReader({self.filepath})"

    def __str__(self):
        return f"VideoReader({self.filepath})"

    def __del__(self):
        self.cap.release()


# TODO: write test cases
class VideoHandler(BaseFileHandler):
    def load_from_fileobj(self, file, **kwargs):
        raise NotImplementedError()

    def save_to_fileobj(self, file, obj, **kwargs):
        raise NotImplementedError()

    def load_from_path(self, filepath, to_rgb=True, **kwargs):
        return VideoReader(filepath, to_rgb=to_rgb)

    def save_to_path(self, filepath, imgs, fps=30, fourcc=None, from_rgb=True, **kwargs):
        if fourcc is None:
            # Use the default codec
            ext = os.path.splitext(filepath)[1][1:]
            default_codecs = {
                "avi": "MJPG",
                "mp4": "avc1",
            }
            fourcc = default_codecs.get(ext, "XVID")

        height, width = imgs[0].shape[:2]
        writer = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*fourcc), fps, (width, height))
        for img in imgs:
            if from_rgb:
                if img.shape[-1] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                elif img.shape[-1] == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
            writer.write(img)
        writer.release()
