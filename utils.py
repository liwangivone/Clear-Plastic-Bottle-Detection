import cv2
import numpy as np
import os


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_image(filepath: str):
    """Load image from disk, return (rgb, gray) numpy arrays."""
    img_bgr = cv2.imread(filepath)
    if img_bgr is None:
        raise ValueError(f"Tidak dapat membaca gambar: {filepath}")
    img_rgb  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return img_rgb, img_gray


def save_image(img_rgb: np.ndarray, filepath: str) -> None:
    """Save RGB numpy array to disk as BGR."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    cv2.imwrite(filepath, cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))


def image_info(img_gray: np.ndarray) -> dict:
    """Return basic metadata about a grayscale image."""
    h, w = img_gray.shape
    return {"width": w, "height": h, "pixels": h * w}
