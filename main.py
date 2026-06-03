import os
import uuid

from flask import Flask, render_template, request, jsonify, send_from_directory

from utils        import allowed_file, load_image, save_image, image_info
from preprocessing import preprocess
from segmentation  import run_canny, run_watershed, build_overlay
from evaluate      import compute_stats

# ── App setup ────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR  = os.path.join(BASE_DIR, "dataset", "raw")
RESULT_DIR  = os.path.join(BASE_DIR, "results")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit


# ── Static file helpers ──────────────────────────────────────────────
@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/results/<path:filename>")
def serve_result(filename):
    return send_from_directory(RESULT_DIR, filename)


# ── Main page ────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Processing endpoint ──────────────────────────────────────────────
@app.route("/process", methods=["POST"])
def process():
    # 1. Validate upload
    if "image" not in request.files:
        return jsonify({"error": "Tidak ada file yang dikirim."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Nama file kosong."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Format file tidak didukung. Gunakan JPG, PNG, atau BMP."}), 400

    # 2. Save uploaded file with unique name
    ext        = file.filename.rsplit(".", 1)[1].lower()
    uid        = uuid.uuid4().hex[:10]
    input_name = f"input_{uid}.{ext}"
    input_path = os.path.join(UPLOAD_DIR, input_name)
    file.save(input_path)

    try:
        # 3. Load
        img_rgb, img_gray = load_image(input_path)
        info = image_info(img_gray)

        # 4. Preprocessing
        img_norm = preprocess(img_gray)

        # 5. Canny
        edges = run_canny(img_norm)

        # 6. Watershed
        markers, boundary = run_watershed(img_norm)

        # 7. Overlay
        result_rgb = build_overlay(img_rgb, edges, boundary)

        # 8. Save result
        result_name = f"result_{uid}.png"
        result_path = os.path.join(RESULT_DIR, result_name)
        save_image(result_rgb, result_path)

        # 9. Stats
        stats = compute_stats(edges, boundary, markers)

        return jsonify({
            "original_url": f"/uploads/{input_name}",
            "result_url":   f"/results/{result_name}",
            "info":         info,
            "stats":        stats,
        })

    except Exception as e:
        return jsonify({"error": f"Gagal memproses gambar: {str(e)}"}), 500


# ── Run ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
