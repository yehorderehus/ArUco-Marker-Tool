import cv2
import numpy as np
import os
from datetime import datetime
from plyer import filechooser

from detection import ArUcoDetection


class Handler:
    def __init__(self) -> None:
        self.extensions = {
            "imread": ["bmp", "jpeg", "jpg", "jpe", "jp2",
                       "png", "webp", "pbm", "pgm", "ppm",
                       "pxm", "pnm", "sr", "ras", "tiff",
                       "tif", "exr", "hdr", "pic"],
            "videocapture": ["gif", "mp4", "avi", "mov", "mkv",
                             "wmv", "flv", "webm", "mpg", "mpeg",
                             "ts", "m4v"],
        }

        self.aruco_detection = ArUcoDetection(
            extensions_dict=self.extensions)

        self.the_asset = None
        self.asset_extension = None
        self.the_media = None
        self.media_extension = None
        self.the_media_output = None

        self.last_saved_timestamp = None
        self.screenshot_counter = 0
        self.screenshots_dir = os.path.abspath("screenshots")

    def init_cap(self, source, name):
        if self.cap_check(name):
            self.cap_del(name)

        cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            return False

        setattr(self, f"cap_{name}", cap)
        setattr(self, f"fps_{name}", cap.get(cv2.CAP_PROP_FPS))
        return True

    def refresh_cap(self, name):
        ret, frame = getattr(self, f"cap_{name}").read()

        if ret:
            return self.read_frame(frame, type=name)
        else:
            return None

    def read_frame(self, frame, type):
        if type == "live":
            if isinstance(self.the_asset, list):
                return self.aruco_detection.aruco_processing(
                    frame, self.get_video("asset"), self.asset_extension)
            return self.aruco_detection.aruco_processing(
                frame, self.the_asset, self.asset_extension)
        else:
            return frame

    def refresh_media_output(self):
        self.the_media_output = None
        self.fps_media_output = None
        self.frame_index_media_output = None

        if isinstance(self.the_media, list):
            self.fps_media_output = self.fps_media
            self.frame_index_media_output = 0

            if isinstance(self.the_asset, list):
                self.the_media_output = [self.aruco_detection.aruco_processing(
                    frame, self.get_video("asset"), self.asset_extension)
                    for frame in self.the_media]

            elif isinstance(self.the_asset, np.ndarray):
                self.the_media_output = [self.aruco_detection.aruco_processing(
                    frame, self.the_asset, self.asset_extension)
                    for frame in self.the_media]
            else:
                self.the_media_output = [self.aruco_detection.aruco_processing(
                    frame, None, None) for frame in self.the_media]

        elif isinstance(self.the_media, np.ndarray):
            frame = self.the_media

            if isinstance(self.the_asset, list):
                self.fps_media_output = self.fps_asset
                self.frame_index_media_output = 0
                self.the_media_output = [self.aruco_detection.aruco_processing(
                    frame, self.get_video("asset"), self.asset_extension)
                    for _ in self.the_asset]

            elif isinstance(self.the_asset, np.ndarray):
                self.the_media_output = self.aruco_detection.aruco_processing(
                    frame, self.the_asset, self.asset_extension)
            else:
                self.the_media_output = self.aruco_detection.aruco_processing(
                    frame, None, None)
        else:
            return

    def write_video(self, file, type):
        if self.init_cap(source=file, name=type) is False:
            return

        setattr(self, f"the_{type}", [])
        setattr(self, f"frame_index_{type}", 0)

        while True:
            frame = self.refresh_cap(name=type)

            if frame is not None:
                getattr(self, f"the_{type}").append(frame)
            else:
                return

    def write_image(self, file, type):
        frame = cv2.imread(file)
        setattr(self, f"the_{type}", frame)

    def get_video(self, type):
        video = getattr(self, f"the_{type}")

        if not video:
            return None

        frame_index = getattr(self, f"frame_index_{type}")
        frame = video[frame_index]
        setattr(self, f"frame_index_{type}", (frame_index + 1) % len(video))
        return frame

    def get_image(self, type):
        return getattr(self, f"the_{type}")

    def select_file(self, type):
        file_path = filechooser.open_file()

        if not file_path:
            return False

        file = file_path[0]
        file_extension = file.split(".")[-1].lower()
        setattr(self, f"{type}_extension", file_extension)

        def manage_file():
            if (type == "asset" or type == "media"):
                if file_extension in self.extensions["imread"]:
                    self.write_image(file, type)
                    self.refresh_media_output()
                elif file_extension in self.extensions["videocapture"]:
                    self.write_video(file, type)
                    self.refresh_media_output()
                else:
                    return False
            else:
                return False

        manage_file()

    def get_format(self):
        if isinstance(self.the_media_output, np.ndarray):
            return "image"
        elif isinstance(self.the_media_output, list):
            return "video"
        else:
            return None

    def capture_frame(self):
        if self.cap_check(name="live"):
            frame = getattr(self, "cap_live").read()[1]
        elif isinstance(self.the_media_output, list):
            frame = getattr(self, "the_media_output")[
                getattr(self, "frame_index_media_output")]
        elif isinstance(self.the_media_output, np.ndarray):
            frame = self.get_image(type="media_output")

        current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if current_timestamp != self.last_saved_timestamp:
            self.screenshot_counter = 0
        else:
            self.screenshot_counter += 1
        self.last_saved_timestamp = current_timestamp

        counter_suffix = f"_{self.screenshot_counter}" if self.screenshot_counter > 0 else ""
        filename = f"screenshot_{current_timestamp}{counter_suffix}.png"
        save_dir = self.screenshots_dir
        save_path = os.path.join(save_dir, filename)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        try:
            cv2.imwrite(save_path, frame)
            return True
        except Exception:
            return False

    def get_fps(self, name):
        return getattr(self, f"fps_{name}")

    def cap_check(self, name):
        return hasattr(self, f"cap_{name}")

    def cap_del(self, name):
        if self.cap_check(name):
            getattr(self, f"cap_{name}").release()
            delattr(self, f"cap_{name}")

    def cam_flip(self, source):
        self.cap_del(source)
        return source ^ 1

    def frame_flip(self, frame):
        return cv2.flip(frame, 0)

    def transfer_aruco_dictionaries(self, dictionaries_cargo):
        self.aruco_detection.set_aruco_dictionaries(dictionaries_cargo)
