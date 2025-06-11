import streamlit as st
import pandas as pd
import urllib.parse
import io

st.set_page_config(page_title="Follow-Up Dokter RM", layout="wide")
st.title("📁 Follow-Up WhatsApp Rekam Medis Dokter")

# === Download Template ===
st.markdown("### 📥 Download Template Dokter")
template_data = pd.DataFrame({
    "Nama Dokter": ["dr. Andi", "dr. Clara"],
    "Nomor WA": ["6281234567890", "6289876543210"],
    "Status": ["Belum upload hasil lab", "Belum isi resume pasien"]
})
buffer = io.BytesIO()
template_data.to_excel(buffer, index=False)
buffer.seek(0)
st.download_button(
    label="⬇️ Download Template Excel",
    data=buffer,
    file_name="template_dokter.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("---")

# === Upload Spreadsheet ===
uploaded_file = st.file_uploader("📤 Upload Spreadsheet Dokter (CSV/XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    # Load file
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
        # Filter belum lengkap
        df_belum = df[~df['Status'].str.lower().str.contains("lengkap")]
        
        if df_belum.empty:
            st.success("🎉 Semua dokter sudah lengkap!")
        else:
            st.markdown("### 👨‍⚕️ Pilih Dokter yang Akan Dikirim")
            selected_dokter = st.multiselect("Pilih Dokter", df_belum['Nama Dokter'].tolist(), default=df_belum['Nama Dokter'].tolist())

            catatan_tambahan = st.text_input("📝 Tambahkan Catatan Tambahan (opsional):", "")

            if st.button("📤 Kirim Pesan WhatsApp ke Semua"):
                for nama in selected_dokter:
                    row = df_belum[df_belum['Nama Dokter'] == nama].iloc[0]
                    nomor = str(row["Nomor WA"]).strip()
                    status = row["Status"]

                    pesan = f"""Assalamu'alaikum {nama},

Mohon segera melengkapi rekam medis pasien Anda.
Status saat ini: *{status}*.

{catatan_tambahan}

Terima kasih 🙏"""

                    encoded_pesan = urllib.parse.quote(pesan)
                    wa_link = f"https://wa.me/{nomor}?text={encoded_pesan}"

                    # Tampilkan linknya
                    st.markdown(f"- [{nama}]({wa_link})", unsafe_allow_html=True)
                
                st.info("Klik nama-nama di atas untuk membuka WhatsApp Web secara manual (dibuka di tab baru).")
