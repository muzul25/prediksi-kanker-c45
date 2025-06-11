import streamlit as st
from fpdf import FPDF
from datetime import date

st.set_page_config(page_title="Penerbitan Surat Keterangan Kematian", layout="centered")

st.title("🪦 Penerbitan Surat Keterangan Kematian")

# Input data jenazah
st.subheader("📋 Data Jenazah")
nama_jenazah = st.text_input("Nama Lengkap")
nik_jenazah = st.text_input("NIK")
tempat_lahir = st.text_input("Tempat Lahir")
tanggal_lahir = st.date_input("Tanggal Lahir")
jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
alamat = st.text_area("Alamat Lengkap")
tanggal_meninggal = st.date_input("Tanggal Meninggal")
penyebab = st.text_input("Penyebab Kematian")

# Input data pelapor
st.subheader("📋 Data Pelapor (Ahli Waris)")
nama_pelapor = st.text_input("Nama Pelapor")
hubungan = st.text_input("Hubungan dengan Jenazah")
alamat_pelapor = st.text_area("Alamat Pelapor")

# Tombol cetak surat
if st.button("🖨️ Buat Surat Keterangan Kematian"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="PEMERINTAH DESA", ln=True, align="C")
    pdf.cell(200, 10, txt="SURAT KETERANGAN KEMATIAN", ln=True, align="C")
    pdf.cell(200, 10, txt="Nomor: .../SKK/VI/2025", ln=True, align="C")
    pdf.ln(10)

    pdf.multi_cell(0, 10, txt=f"Yang bertanda tangan di bawah ini menerangkan bahwa pada hari ini telah meninggal dunia seseorang dengan identitas sebagai berikut:\n\n"
                              f"Nama Lengkap    : {nama_jenazah}\n"
                              f"NIK             : {nik_jenazah}\n"
                              f"Tempat/Tgl Lahir: {tempat_lahir}, {tanggal_lahir.strftime('%d-%m-%Y')}\n"
                              f"Jenis Kelamin   : {jenis_kelamin}\n"
                              f"Alamat          : {alamat}\n"
                              f"Tanggal Meninggal: {tanggal_meninggal.strftime('%d-%m-%Y')}\n"
                              f"Penyebab        : {penyebab}\n\n"
                              f"Pelapor dari kematian ini adalah:\n"
                              f"Nama            : {nama_pelapor}\n"
                              f"Hubungan        : {hubungan}\n"
                              f"Alamat Pelapor  : {alamat_pelapor}\n\n"
                              f"Demikian surat keterangan ini dibuat untuk dapat dipergunakan sebagaimana mestinya.")

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Medan, {date.today().strftime('%d-%m-%Y')}", ln=True, align="R")
    pdf.cell(200, 10, txt="Kepala Desa", ln=True, align="R")
    pdf.ln(20)
    pdf.cell(200, 10, txt="(............................)", ln=True, align="R")

    filename = "surat_keterangan_kematian.pdf"
    pdf.output(filename)

    with open(filename, "rb") as f:
        st.download_button(
            label="📥 Download Surat Kematian (PDF)",
            data=f,
            file_name=filename,
            mime="application/pdf"
        )
