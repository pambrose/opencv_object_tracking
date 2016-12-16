import cv2
import numpy as np


class ContourFinder:
    def __init__(self, bgr_color, hsv_range):
        bgr_img = np.uint8([[bgr_color]])
        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        hsv_value = hsv_img[0, 0, 0]
        self._lower = np.array([hsv_value - hsv_range, 100, 100])
        self._upper = np.array([hsv_value + hsv_range, 255, 255])

    def get_contour(self, image):
        # Convert from BGR to HSV colorspace
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only target colors
        in_range_mask = cv2.inRange(hsv_image, self._lower, self._upper)

        # Bitwise-AND mask and original image
        in_range_result = cv2.bitwise_and(image, image, mask=in_range_mask)

        # Convert to grayscale
        grayscale = cv2.cvtColor(in_range_result, cv2.COLOR_BGR2GRAY)

        # Get all contours
        contours = cv2.findContours(grayscale, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

        # Return max contour
        return self._find_max_contour(contours)

    def _find_max_contour(self, contours):
        max_index = -1
        max_val = 0
        if contours:
            for i, c in enumerate(contours):
                moments = cv2.moments(c)
                area = moments["m00"]
                if 0 <= max_val < area:
                    max_val = area
                    max_index = i
        return contours[max_index] if max_index != -1 else None