import streamlit as st
import pandas as pd
import urllib.parse
import io
from datetime import datetime

# === Setup App ===
st.set_page_config(page_title="Follow-Up Dokter RM", layout="wide")
st.title("📁 Follow-Up WhatsApp Rekam Medis Dokter")

# === Download Template Dokter ===
st.markdown("### 📥 Download Template Excel Dokter")
template_data = pd.DataFrame({
    "Nama Dokter": ["dr. Andi", "dr. Clara"],
    "Nomor WA": ["6281234567890", "6289876543210"]
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
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File berhasil dimuat!")

    required_cols = ['Nama Dokter', 'Nomor WA']
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ Spreadsheet harus memiliki kolom: {', '.join(required_cols)}")
    else:
        st.markdown("### 👨‍⚕️ Pilih Dokter yang Akan Dikirimi Notifikasi")
        selected_dokter = st.multiselect("Pilih Dokter", df['Nama Dokter'].tolist(), default=df['Nama Dokter'].tolist())

        st.markdown("### 📅 Tambahkan Jadwal Follow-Up")

        jumlah_tanggal = st.number_input("Berapa tanggal follow-up?", min_value=1, max_value=10, value=1, step=1)

        jadwal_list = []

        # Nama hari manual (cross-platform)
        nama_hari_dict = {
            0: "Senin", 1: "Selasa", 2: "Rabu",
            3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"
        }

        for i in range(jumlah_tanggal):
            with st.expander(f"Tanggal #{i+1}"):
                tanggal = st.date_input(f"Pilih tanggal ke-{i+1}", key=f"tgl_{i}")
                jumlah = st.number_input(f"Jumlah berkas pada tanggal tersebut", min_value=1, key=f"jumlah_{i}")
                if tanggal:
                    nama_hari = nama_hari_dict[tanggal.weekday()]
                    tanggal_fmt = tanggal.strftime("%d/%m/%Y")
                    jadwal = f"Hari {nama_hari}, tanggal {tanggal_fmt} Sebanyak {jumlah} Berkas"
                    jadwal_list.append(jadwal)

        catatan_tambahan = "\n".join(jadwal_list)

        if st.button("📤 Kirim Pesan WhatsApp ke Semua Dokter Terpilih"):
            st.markdown("### 🔗 Link WhatsApp:")
            for nama in selected_dokter:
                row = df[df['Nama Dokter'] == nama].iloc[0]
                nomor = str(row["Nomor WA"]).replace("+", "").replace(" ", "").replace("-", "").strip()

                pesan = f"""Assalamu'alaikum {nama},

Saya dari staff KLPCM Rekam Medis ingin menginformasikan bahwa terdapat berkas rekam medis yang belum lengkap.
Mohon bantuannya untuk melengkapi sesuai ketentuan maksimal 2x24 jam sejak pelayanan.
Status saat ini: *Belum Lengkap*.

{catatan_tambahan}

Terima kasih sebelumnya, dok 🙏"""

                encoded_pesan = urllib.parse.quote(pesan, safe='')
                wa_link = f"https://wa.me/{nomor}?text={encoded_pesan}"

                st.markdown(f"- [{nama}]({wa_link})", unsafe_allow_html=True)

            st.info("Klik nama-nama di atas untuk membuka WhatsApp Web dengan isi pesan.")
