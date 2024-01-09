import cv2
import numpy as np

from augmentation import FrameAugmentation


class ArUcoDetection:
    def __init__(self, extensions_dict) -> None:
        self.extensions = extensions_dict

        # Predefined ArUco dictionary, changes as needed
        self.set_aruco_dictionaries(["DICT_ARUCO_ORIGINAL"])

    def set_aruco_dictionaries(self, dictionaries):
        self.aruco_dictionaries = [cv2.aruco.getPredefinedDictionary(
            cv2.aruco.__getattribute__(dictionary)) for dictionary in dictionaries]

    def aruco_processing(self, frame, the_asset, asset_extension):
        if frame is None:
            return None

        processed_frame = frame.copy()  # Copy the frame to avoid mixing up

        for aruco_dict in self.aruco_dictionaries:
            self.aruco_properties(processed_frame, aruco_dict)

            # 4 loops for 4 corners
            for aruco_corner in self.aruco_corners:
                if asset_extension in self.extensions["imread"] \
                        or asset_extension in self.extensions["videocapture"]:
                    processed_frame = FrameAugmentation().frame_augmentation(
                        aruco_corner, processed_frame, the_asset)
                else:
                    processed_frame = self.aruco_highlightning(
                        processed_frame, aruco_corner)

        return processed_frame

    def aruco_properties(self, frame, aruco_dict):
        self.aruco_corners, _, _ = \
            cv2.aruco.detectMarkers(
                frame, aruco_dict,
                parameters=cv2.aruco.DetectorParameters()
            )

    def aruco_highlightning(self, processed_frame, aruco_corner):
        aruco_polygon = [np.int32(aruco_corner)]
        aruco_side_length = np.linalg.norm(
            aruco_corner[0][0] - aruco_corner[0][1])

        processed_frame = cv2.polylines(
            processed_frame,
            aruco_polygon,
            isClosed=True,
            color=(0, 255, 0),
            thickness=int(aruco_side_length * 0.01)
        )

        return processed_frame
