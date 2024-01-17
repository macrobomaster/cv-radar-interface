import cv2
import numpy as np

class Radar():

    def __init__(self, xy: list[list[int]], arena_width: list[int], arena_height: list[int]):
        x = [i[0] for i in xy]
        y = [i[1] for i in xy]

        self.arena_image_coords = np.array([[x[0], y[0]], [x[1], y[1]], [x[2], y[2]], [x[3], y[3]]], dtype=np.float32)
        self.arena_coords = np.array([[0, 0], [arena_width - 1, 0], [arena_width - 1, arena_height - 1], [0, arena_height - 1]], dtype=np.float32)
        self.homography_matrix, _ = cv2.findHomography(self.arena_image_coords, self.arena_coords)

    def transform(self, input_point: list[int]):
        point_on_image = np.array([[input_point[0], input_point[1]]], dtype=np.float32).reshape(-1, 1, 2)
        transformed_point = cv2.perspectiveTransform(point_on_image, self.homography_matrix)

        return transformed_point