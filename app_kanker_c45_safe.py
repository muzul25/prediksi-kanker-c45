import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Follow-Up WhatsApp RM", layout="centered")
st.title("📁 Follow-Up Rekam Medis via WhatsApp")

# Upload file spreadsheet
uploaded_file = st.file_uploader("📤 Upload Spreadsheet Dokter (CSV/XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File berhasil dimuat!")

    # Validasi kolom
    required_cols = ['Nama Dokter', 'Nomor WA', 'Status']
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ Kolom wajib: {', '.join(required_cols)}")
    else:
        # Filter dokter belum lengkap
        df_belum = df[~df['Status'].str.lower().str.contains("lengkap")]

        if df_belum.empty:
            st.success("🎉 Semua data dokter lengkap!")
        else:
            st.markdown("### 👨‍⚕️ Daftar Dokter Belum Lengkap")
            selected = st.selectbox("Pilih Dokter", df_belum['Nama Dokter'])

            row = df_belum[df_belum['Nama Dokter'] == selected].iloc[0]
            nomor = str(row['Nomor WA']).strip()
            status = row['Status']
            nama = row['Nama Dokter']

            # Template pesan
            pesan = f"""Assalamu'alaikum {nama},

Mohon segera melengkapi rekam medis pasien Anda.
Status saat ini: *{status}*.

Terima kasih 🙏"""

            # Encode pesan untuk URL
            encoded_pesan = urllib.parse.quote(pesan)
            wa_link = f"https://wa.me/{nomor}?text={encoded_pesan}"

            st.text_area("📨 Isi Pesan", pesan, height=150)
            st.markdown(f"[📤 Kirim via WhatsApp]({wa_link})", unsafe_allow_html=True)
