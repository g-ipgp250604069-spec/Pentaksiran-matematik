from datetime import datetime
import google.generativeai as genai
from PIL import Image
import pandas as pd
import streamlit as st

# 1. Konfigurasi Halaman Web Streamlit
st.set_page_config(
    page_title="Penilaian Matematik PBD", page_icon="📐", layout="centered"
)

st.title("📐 Sistem Semakan & Pentaksiran Lukisan Matematik")
st.write(
    "Sila masukkan nama anda, pilih soalan, muat naik gambar lukisan,"
    " dan dapatkan maklum balas serta markah serta-merta."
)

# 2. Masukkan Gemini API Key (Kunci API Cikgu)
API_KEY = st.text_input("Masukkan Gemini API Key Cikgu:", type="password")

if API_KEY:
  genai.configure(api_key=API_KEY)

  st.divider()
  st.subheader("📝 Maklumat Murid & Tugasan")

  # --- RUANG KHAS UNTUK MURID ISI NAMA ---
  nama_murid = st.text_input(
      "Nama Penuh Murid:",
      placeholder="Sila masukkan nama penuh anda di sini...",
  )

  # Pilihan Soalan (Merujuk kepada tugasan 6a, 6b, 6c)[cite: 1]
  soalan_pilihan = st.selectbox(
      "Pilih Soalan Tugasan yang Ingin Disemak:",
      [
          "Soalan 6(a) - Pentagon Sekata (Sempadan Taman Bunga)",
          "Soalan 6(b) - Pelan Bulatan Kolam Renang & Ukuran",
          "Soalan 6(c) - Pemilihan Saiz Papan Pelapik Kek",
      ],
  )

  # Bahagian Muat Naik Gambar oleh Murid
  uploaded_file = st.file_uploader(
      "Sila snap dan muat naik gambar jawapan/lukisan anda di sini (JPG/PNG):",
      type=["jpg", "jpeg", "png"],
  )

  if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar lukisan/jawapan yang dihantar", width=400)

    if st.button("🚀 Semak Jawapan Sekarang"):
      # Semak sama ada murid sudah isi nama atau belum
      if not nama_murid.strip():
        st.warning(
            "⚠️ Sila masukkan Nama Penuh anda terlebih dahulu sebelum menekan"
            " butang semak!"
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

            model = genai.GenerativeModel("gemini-3.6-flash")
            response = model.generate_content([prompt, image])
            hasil_ai = response.text

            st.success("Semakan berjaya!")
            st.markdown("### 📋 Keputusan & Maklum Balas AI:")
            st.markdown(hasil_ai)

            # --- SIMPAN DATA KE REKOD EXCEL ---
            if "data_rekod" not in st.session_state:
              st.session_state.data_rekod = []

            # Masukkan data lengkap beserta nama murid
            st.session_state.data_rekod.append({
                "Tarikh/Masa": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nama Murid": nama_murid,
                "Soalan": soalan_pilihan,
                "Maklum Balas & Markah AI": hasil_ai,
            })

          except Exception as e:
            st.error(f"Berlaku ralat: {e}")

  # Bahagian untuk Cikgu Muat Turun Fail Excel
  if (
      "data_rekod" in st.session_state
      and len(st.session_state.data_rekod) > 0
  ):
    st.divider()
    st.subheader("📊 Panel Guru: Muat Turun Rekod Markah")
    df = pd.DataFrame(st.session_state.data_rekod)

    output = pd.ExcelWriter("rekod_pbd_murid.xlsx", engine="openpyxl")
    df.to_excel(output, index=False, sheet_name="Markah Murid")
    output.close()

    with open("rekod_pbd_murid.xlsx", "rb") as f:
      st.download_button(
          label="📥 Muat Turun Fail Excel Rekod PBD (.xlsx)",
          data=f,
          file_name="rekod_pbd_murid.xlsx",
          mime=(
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ),
      )
else:
  st.info(
      "Sila masukkan Gemini API Key Cikgu di atas untuk memulakan aplikasi."
  )
