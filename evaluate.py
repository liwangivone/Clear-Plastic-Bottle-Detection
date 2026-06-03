import numpy as np


def compute_stats(edges: np.ndarray,
                  boundary: np.ndarray,
                  markers: np.ndarray) -> dict:
    """
    Compute segmentation statistics shown on the result page.

    Returns a dict with:
      - canny_pixels    : number of edge pixels detected by Canny
      - boundary_pixels : number of watershed boundary pixels
      - num_segments    : number of distinct segments (regions)
    """
    return {
        "canny_pixels":    int(np.count_nonzero(edges)),
        "boundary_pixels": int(np.sum(boundary == 255)),
        "num_segments":    int(markers.max()),
    }
