import numpy as np
import cv2

# Reading image
font = cv2.FONT_HERSHEY_COMPLEX
img2 = cv2.imread('test.jpg', cv2.IMREAD_COLOR)

# Reading same image in another
# variable and converting to gray scale.
img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)

# Converting image to a binary image
# ( black and white only image).
_, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

# Detecting contours in image.
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
print(contours)
