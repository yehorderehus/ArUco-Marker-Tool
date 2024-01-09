import cv2
import numpy as np
from PIL import Image


class FrameAugmentation:
    def __init__(self) -> None:
        pass

    def frame_augmentation(self, bbox, shot, augment):
        top_left = bbox[0][0][0], bbox[0][0][1]
        top_right = bbox[0][1][0], bbox[0][1][1]
        bottom_right = bbox[0][2][0], bbox[0][2][1]
        bottom_left = bbox[0][3][0], bbox[0][3][1]

        # Open an rectangular from augment and get its dimensions
        rectangle = Image.fromarray(augment)
        width, height = rectangle.size
        side_length = max(width, height)

        # Calculate position for centering the rectangular on a background
        x_offset = (side_length - width) // 2
        y_offset = (side_length - height) // 2

        # Make the background and paste the rectangular onto it
        background = Image.new("RGB", (side_length, side_length), (0, 0, 0))
        background.paste(rectangle, (x_offset, y_offset))

        # Convert edited augment to numpy array
        augment = np.array(background)

        # Find numpy arrays of the corner points of the shot and the augment
        points_shot = np.array([top_left, top_right,
                                bottom_right, bottom_left])
        points_augment = np.array([[0, 0], [side_length, 0],
                                   [side_length, side_length],
                                   [0, side_length]])

        # Calculate the transformation matrix and warp the augment
        matrix = cv2.getPerspectiveTransform(points_augment.astype(
            np.float32), points_shot.astype(np.float32))
        augment = cv2.warpPerspective(augment, matrix,
                                      (shot.shape[1], shot.shape[0]))

        # Fill the shot with the processed augment
        cv2.fillConvexPoly(shot, points_shot.astype(int), (0, 0, 0), 16)

        return shot + augment
