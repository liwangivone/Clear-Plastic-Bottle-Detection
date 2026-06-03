import cv2
import numpy as np


def run_canny(img_norm: np.ndarray,
              low_threshold: int = 30,
              high_threshold: int = 100) -> np.ndarray:
    """
    Stage 3 — Canny Edge Detection.
    Returns binary edge map (0 / 255).
    """
    return cv2.Canny(img_norm, low_threshold, high_threshold)


def run_watershed(img_norm: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Stage 4-5 — Watershed segmentation.
    Steps:
      1. Otsu thresholding  → binary mask
      2. Morphological open + close  → remove noise
      3. Distance transform  → estimate foreground
      4. Connected components  → markers
      5. Watershed  → label regions
    Returns (markers array, boundary map 0/255).
    """
    kernel = np.ones((3, 3), np.uint8)

    # --- Otsu threshold ---
    _, img_bin = cv2.threshold(
        img_norm, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # --- Morphological cleanup ---
    img_clean = cv2.morphologyEx(img_bin,   cv2.MORPH_OPEN,  kernel, iterations=2)
    img_clean = cv2.morphologyEx(img_clean, cv2.MORPH_CLOSE, kernel, iterations=2)

    # --- Sure background & foreground ---
    sure_bg    = cv2.dilate(img_clean, kernel, iterations=5)
    dist       = cv2.distanceTransform(img_clean, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.3 * dist.max(), 255, 0)
    sure_fg    = np.uint8(sure_fg)
    unknown    = cv2.subtract(sure_bg, sure_fg)

    # --- Markers ---
    _, markers = cv2.connectedComponents(sure_fg)
    markers    = markers + 1
    markers[unknown == 255] = 0

    # --- Watershed ---
    cv2.watershed(cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR), markers)

    # --- Extract boundary ---
    boundary = np.zeros_like(img_norm, dtype=np.uint8)
    boundary[markers == -1] = 255

    return markers, boundary


def build_overlay(img_rgb: np.ndarray,
                  edges: np.ndarray,
                  boundary: np.ndarray) -> np.ndarray:
    """
    Stage 6 — Visualisation overlay on original RGB image.
      - Watershed boundary  → red  [255, 40, 40]
      - Canny edges         → cyan [0, 230, 255]
    Returns RGB result image.
    """
    kernel   = np.ones((3, 3), np.uint8)
    result   = img_rgb.copy()

    boundary_dilated = cv2.dilate(boundary, kernel, iterations=1)
    edges_dilated    = cv2.dilate(edges,    np.ones((2, 2), np.uint8), iterations=1)

    result[boundary_dilated == 255] = [255, 40,  40]
    result[edges_dilated    >  0]   = [0,  230, 255]

    return result
