import cv2
import numpy as np


def preprocess(img_gray: np.ndarray) -> np.ndarray:
    """
    Stage 2 — Preprocessing pipeline:
      1. CLAHE  : normalize local contrast
      2. Gaussian Blur (5x5) : suppress high-frequency noise
      3. Normalize  : scale pixel values to 0-255
    Returns preprocessed grayscale image.
    """
    clahe     = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_gray)
    img_blur  = cv2.GaussianBlur(img_clahe, (5, 5), sigmaX=1)
    img_norm  = cv2.normalize(img_blur, None, 0, 255, cv2.NORM_MINMAX)
    return img_norm
