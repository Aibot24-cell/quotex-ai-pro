import cv2
import numpy as np

def preprocess_chart_image(image_pil):
    img_array = np.array(image_pil)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return {
        "original_array": img_array,
        "grayscale": gray,
        "edges": edges,
        "edge_count": int(np.count_nonzero(edges))
    }