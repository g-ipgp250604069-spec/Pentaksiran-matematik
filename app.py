import google.generativeai as genai
from PIL import Image
import streamlit as st

# 1. Konfigurasi Halaman Web Streamlit
st.set_page_config(
    page_title="Penilaian Matematik PBD", page_icon="📐", layout="centered"
)

st.title("📐 Sistem Semakan & Pentaksiran Lukisan Matematik")
st.write(
    "Sila pilih soalan, muat naik gambar lukisan/jawapan anda, dan dapatkan"
    " maklum balas serta markah serta-merta."
)

# 2. Mengambil API Key secara selamat dari sistem latar belakang Streamlit
try:
  API_KEY = st.secrets["GEMINI_API_KEY"]
  genai.configure(api_key=API_KEY)

  # 3. Pilihan Soalan (Merujuk kepada tugasan 6a, 6b, 6c)
  soalan_pilihan = st.selectbox(
      "Pilih Soalan Tugasan:",
      [
          "Soalan 6(a) - Pentagon Sekata (Sempadan Taman Bunga)",
          "Soalan 6(b) - Pelan Bulatan Kolam Renang & Ukuran",
          "Soalan 6(c) - Pemilihan Saiz Papan Pelapik Kek",
      ],
  )

  # 4. Bahagian Muat Naik Gambar oleh Murid
  uploaded_file = st.file_uploader(
      "Sila snap dan muat naik gambar jawapan/lukisan anda di sini (JPG/PNG):",
      type=["jpg", "jpeg", "png"],
  )

  if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(
        image,
        caption="Gambar lukisan/jawapan yang dihantar",
        use_container_width=True,
    )

    if st.button("🚀 Semak Jawapan Sekarang"):
      with st.spinner("AI sedang menilai lukisan dan jawapan anda..."):
        try:
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
                    3. **Ulasan & Sebab Markah:** (Berikan pujian pada bahagian yang betul dan panduan penambahbaikan jika ada kesilapan).
                    """

          model = genai.GenerativeModel("gemini-3.8-flash")
          response = model.generate_content([prompt, image])

          st.success("Semakan berjaya!")
          st.markdown("### 📋 Keputusan & Maklum Balas AI:")
          st.markdown(response.text)

        except Exception as e:
          st.error(f"Berlaku ralat semasa semakan: {e}")

except Exception:
  st.error(
      "⚠️ Ralat Pelayan: Gemini API Key belum dikonfigurasikan di dalam tetapan"
      " Streamlit Secrets."
  )
