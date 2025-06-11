import streamlit as st
import pandas as pd
import pywhatkit
import datetime

st.set_page_config(page_title="Follow-Up RM Dokter", layout="wide")
st.title("📋 Aplikasi Follow-Up Dokter untuk Rekam Medis Tidak Lengkap")

uploaded_file = st.file_uploader("Unggah File Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Tampilkan isi file
    st.subheader("Data Pasien")
    st.dataframe(df)

    # Filter pasien dengan status "Tidak Lengkap"
    df_tidak_lengkap = df[df['Status RM'].str.lower() == "tidak lengkap"]

    if not df_tidak_lengkap.empty:
        st.subheader("📌 Pasien dengan RM Tidak Lengkap")
        st.dataframe(df_tidak_lengkap)

        # Kelompokkan berdasarkan dokter
        grouped = df_tidak_lengkap.groupby(['Nama Dokter', 'No WA Dokter'])

        st.subheader("📲 Kirim Follow-Up via WhatsApp")

        for (dokter, no_wa), group in grouped:
            st.markdown(f"**{dokter} ({no_wa})**")

            pesan = f"Assalamu'alaikum {dokter},\nBerikut daftar pasien Anda dengan rekam medis yang belum lengkap:\n"
            for _, row in group.iterrows():
                pesan += f"- {row['Nama Pasien']} (RM: {row['No RM']})\n"
            pesan += "\nMohon segera dilengkapi. Terima kasih 🙏"

            st.text_area("Pesan WhatsApp", value=pesan, height=150, key=no_wa)

            if st.button(f"Kirim ke {dokter}", key=f"kirim_{no_wa}"):
                try:
                    # Kirim pesan via WhatsApp Web (jadwalkan 1 menit dari waktu sekarang)
                    now = datetime.datetime.now()
                    jam = now.hour
                    menit = now.minute + 1
                    pywhatkit.sendwhatmsg(f"+{no_wa}", pesan, jam, menit, wait_time=10, tab_close=True)
                    st.success(f"Pesan ke {dokter} berhasil dijadwalkan!")
                except Exception as e:
                    st.error(f"Gagal mengirim pesan ke {dokter}: {e}")
    else:
        st.info("✅ Semua rekam medis sudah lengkap.")
