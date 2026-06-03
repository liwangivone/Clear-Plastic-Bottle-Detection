/* ── DOM refs ─────────────────────────────────────────────────────── */
const dropZone    = document.getElementById("dropZone");
const fileInput   = document.getElementById("fileInput");
const browseBtn   = document.getElementById("browseBtn");
const previewWrap = document.getElementById("previewWrap");
const previewImg  = document.getElementById("previewImg");
const previewInfo = document.getElementById("previewInfo");
const resetBtn    = document.getElementById("resetBtn");
const processBtn  = document.getElementById("processBtn");
const uploadCard  = document.getElementById("uploadCard");
const loader      = document.getElementById("loader");
const resultCard  = document.getElementById("resultCard");
const imgOriginal = document.getElementById("imgOriginal");
const imgResult   = document.getElementById("imgResult");
const statsGrid   = document.getElementById("statsGrid");
const downloadBtn = document.getElementById("downloadBtn");
const newBtn      = document.getElementById("newBtn");
const errorBox    = document.getElementById("errorBox");
const errorMsg    = document.getElementById("errorMsg");

let selectedFile  = null;

/* ── Permission alert ─────────────────────────────────────────────── */
window.addEventListener("DOMContentLoaded", () => {
  const granted = sessionStorage.getItem("fileAccessGranted");
  if (!granted) {
    const ok = window.confirm(
      "🔒 Izin Akses Diperlukan\n\n" +
      "Aplikasi ini memerlukan akses ke file di perangkat kamu " +
      "untuk memproses gambar botol plastik.\n\n" +
      "Klik OK untuk melanjutkan, atau Batal untuk menolak."
    );
    if (!ok) {
      document.querySelector("main").innerHTML =
        `<div class="card" style="text-align:center;padding:3rem;">
           <p style="font-size:1.5rem;margin-bottom:.75rem;">🚫</p>
           <p style="color:#6B7280;">Akses file ditolak. Muat ulang halaman untuk mencoba lagi.</p>
         </div>`;
      return;
    }
    sessionStorage.setItem("fileAccessGranted", "true");
  }
});

/* ── Open file picker ─────────────────────────────────────────────── */
browseBtn.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("click", (e) => {
  if (e.target !== browseBtn) fileInput.click();
});

/* ── Drag & drop ──────────────────────────────────────────────────── */
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  if (file) handleFileSelect(file);
});

/* ── File input change ────────────────────────────────────────────── */
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFileSelect(fileInput.files[0]);
});

/* ── Handle selected file ─────────────────────────────────────────── */
function handleFileSelect(file) {
  const allowed = ["image/jpeg", "image/png", "image/bmp",
                   "image/tiff", "image/webp"];
  if (!allowed.includes(file.type)) {
    showError("Format file tidak didukung. Gunakan JPG, PNG, atau BMP.");
    return;
  }
  if (file.size > 16 * 1024 * 1024) {
    showError("Ukuran file melebihi batas 16 MB.");
    return;
  }

  selectedFile = file;
  hideError();

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewInfo.textContent =
      `${file.name}  ·  ${(file.size / 1024).toFixed(1)} KB`;
    dropZone.hidden    = true;
    previewWrap.hidden = false;
    resultCard.hidden  = true;
  };
  reader.readAsDataURL(file);
}

/* ── Reset ────────────────────────────────────────────────────────── */
resetBtn.addEventListener("click", resetState);
newBtn.addEventListener("click", resetState);

function resetState() {
  selectedFile       = null;
  fileInput.value    = "";
  previewImg.src     = "";
  previewWrap.hidden = true;
  dropZone.hidden    = false;
  resultCard.hidden  = true;
  loader.hidden      = true;
  hideError();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ── Process ──────────────────────────────────────────────────────── */
processBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  // UI state: loading
  previewWrap.hidden = true;
  loader.hidden      = false;
  resultCard.hidden  = true;
  hideError();
  processBtn.disabled = true;

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const res  = await fetch("/process", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok || data.error) {
      throw new Error(data.error || "Terjadi kesalahan pada server.");
    }

    // Show results
    imgOriginal.src  = data.original_url;
    imgResult.src    = data.result_url;
    downloadBtn.href = data.result_url;

    renderStats(data.stats, data.info);

    loader.hidden     = false;
    loader.hidden     = true;
    resultCard.hidden = false;
    resultCard.scrollIntoView({ behavior: "smooth", block: "start" });

  } catch (err) {
    loader.hidden = true;
    previewWrap.hidden = false;
    showError(err.message);
  } finally {
    processBtn.disabled = false;
  }
});

/* ── Render stats cards ───────────────────────────────────────────── */
function renderStats(stats, info) {
  const items = [
    { value: formatNumber(stats.canny_pixels),    label: "Pixel Canny (cyan)" },
    { value: formatNumber(stats.boundary_pixels), label: "Pixel Boundary (merah)" },
    { value: stats.num_segments,                  label: "Jumlah Segmen" },
    { value: `${info.width} × ${info.height}`,    label: "Resolusi Gambar" },
    { value: formatNumber(info.pixels),            label: "Total Pixel" },
  ];

  statsGrid.innerHTML = items.map(item => `
    <div class="stat-card">
      <span class="stat-value">${item.value}</span>
      <span class="stat-label">${item.label}</span>
    </div>
  `).join("");
}

/* ── Helpers ──────────────────────────────────────────────────────── */
function formatNumber(n) {
  return Number(n).toLocaleString("id-ID");
}

function showError(msg) {
  errorMsg.textContent = "⚠️  " + msg;
  errorBox.hidden = false;
}

function hideError() {
  errorBox.hidden = true;
  errorMsg.textContent = "";
}
