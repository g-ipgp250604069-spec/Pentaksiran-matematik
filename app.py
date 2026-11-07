from datetime import datetime
import google.generativeai as genai
from PIL import Image
import streamlit as st

# ==========================================
# TETAPAN KUNCI API (MENGGUNAKAN STREAMLIT SECRETS)
# ==========================================
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# ==========================================
# PAPARAN ANTARA MUKA APLIKASI (UI)
# ==========================================
st.set_page_config(
    page_title="Penilaian Matematik PBD", page_icon="📐", layout="centered"
)

st.title("📐 Sistem Semakan & Pentaksiran Lukisan Matematik")
st.write(
    "Sila masukkan nama anda, pilih soalan, ambil gambar lukisan menggunakan"
    " kamera, dan dapatkan maklum balas serta markah serta-merta."
)

st.divider()
st.subheader("📝 Maklumat Murid & Tugasan")

# Ruang Nama Murid
nama_murid = st.text_input(
    "Nama Penuh Murid:", placeholder="Sila masukkan nama penuh anda di sini..."
)

# Pilihan Soalan (Merujuk kepada tugasan 6a, 6b, 6c)[cite: 1]
soalan_pilihan = st.selectbox(
    "Pilih Soalan Tugasan yang Ingin Disemak:",
    [
        "Soalan 6(a) - Pentagon Sekata (Sempadan Taman Bunga)[cite: 1]",
        "Soalan 6(b) - Pelan Bulatan Kolam Renang & Ukuran[cite: 1]",
        "Soalan 6(c) - Pemilihan Saiz Papan Pelapik Kek[cite: 1]",
    ],
)

st.divider()
st.subheader("📸 Ambil Gambar Lukisan Anda")
st.write(
    "Tekan butang **'Take Photo'** di bawah untuk membuka kamera peranti anda."
)

# --- FUNGSI KAMERA TERUS DALAM APLIKASI ---
uploaded_file = st.camera_input("Kamera Penilaian Lukisan")

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.success("Gambar berjaya diambil! Sila semak paparan di atas.")

  if st.button("🚀 Semak Jawapan Sekarang"):
    if not nama_murid.strip():
      st.warning(
          "⚠️ Sila masukkan Nama Penuh anda terlebih dahulu di atas sebelum"
          " menekan butang semak!"
      )
    else:
      with st.spinner("AI sedang menilai lukisan dan jawapan anda..."):
        try:
          # Prompt & Rubrik Pemarkahan (0 - 5)
          prompt = f"""
                        Anda ialah seorang guru matematik yang tegas tetapi mesra. Tugas anda adalah menyemak tugasan murid untuk: {soalan_pilihan}.
                        
                        Sila nilai gambar lukisan atau jawapan murid ini berdasarkan rubrik skala 0 hingga 5 berikut:
                        - Markah 5: Cemerlang, tepat, dan memenuhi semua kriteria kehendak soalan.
                        - Markah 4: Baik, tetapi ada sedikit ralat kecil pada lukisan/pengiraan.
                        - Markah 3: Sederhana, konsep asas ada tetapi kurang lengkap atau kurang tepat.
                        - Markah 2: Lemah, banyak ralat atau terpesong daripada kehendak soalan.
                        - Markah 1: Mencuba tetapi jawapan/lakaran hampir sepenuhnya tidak tepat.
                        - Markah 0: Tiada jawapan atau kosong.

                        Sila berikan output dalam format ringkas berikut:
                        1. **Status:** [LULUS / PERLU PENAMBAHBAIKAN]
                        2. **Markah Diperoleh:** [X / 5]
                        3. **Ulasan & Sebab Markah:** (Berikan pujian pada bahagian yang betul dan panduan penambahbaikan).
                        """

          model = genai.GenerativeModel("gemini-3.5-flash")
          response = model.generate_content([prompt, image])
          hasil_ai = response.text

          st.success(f"Tahniah, {nama_murid}! Semakan selesai.")
          st.markdown("### 📋 Keputusan & Maklum Balas AI:")
          st.markdown(hasil_ai)

        except Exception as e:
          st.error(
              f"Berlaku ralat semasa memproses gambar. Sila cuba lagi. Ralat:"
              f" {e}"
          )
