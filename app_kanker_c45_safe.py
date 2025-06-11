import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Follow-Up Berkas RM", layout="centered")
st.title("📁 Aplikasi Follow-Up Kelengkapan Rekam Medis")

# Simpan data di session_state
if 'data_dokter' not in st.session_state:
    st.session_state.data_dokter = pd.DataFrame(columns=[
        'Nama Dokter', 'Nomor WA', 'Status Berkas', 'Catatan'
    ])

# SECTION 1: Tambah Dokter
with st.expander("➕ Tambah Dokter Baru", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nama_dokter = st.text_input("Nama Dokter")
        no_wa = st.text_input("Nomor WA (cth: 6281234567890)")
    with col2:
        status = st.selectbox("Status Berkas", ["Belum Lengkap", "Lengkap", "Belum anamnessa", "Belum Isi resume pasien"])
        catatan = st.text_input("Catatan (opsional)")

    if st.button("➕ Tambah ke Daftar"):
        if nama_dokter and no_wa:
            new_row = {
                'Nama Dokter': nama_dokter,
                'Nomor WA': no_wa,
                'Status Berkas': status,
                'Catatan': catatan
            }
            st.session_state.data_dokter = pd.concat([
                st.session_state.data_dokter,
                pd.DataFrame([new_row])
            ], ignore_index=True)
            st.success("✅ Dokter berhasil ditambahkan.")
        else:
            st.warning("❗ Nama Dokter dan Nomor WA wajib diisi.")

# SECTION 2: Daftar Dokter
st.markdown("### 👥 Daftar Dokter")
st.dataframe(st.session_state.data_dokter, use_container_width=True)

# Download CSV
csv = st.session_state.data_dokter.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download CSV Dokter", data=csv, file_name="data_dokter.csv", mime='text/csv')

# SECTION 3: Follow-Up WhatsApp
st.markdown("### 📲 Follow-Up WhatsApp")

df_tidak_lengkap = st.session_state.data_dokter[
    ~st.session_state.data_dokter['Status Berkas'].str.lower().str.contains("lengkap")
]

if not df_tidak_lengkap.empty:
    dokter_pilihan = st.selectbox("Pilih Dokter yang Belum Lengkap", df_tidak_lengkap['Nama Dokter'].unique())
    catatan_tambahan = st.text_area("📝 Tambahkan Catatan Tambahan (Opsional)")

    if st.button("📤 Buat Pesan Follow-Up"):
        row = df_tidak_lengkap[df_tidak_lengkap['Nama Dokter'] == dokter_pilihan].iloc[0]
        pesan = f"""Assalamu'alaikum {row['Nama Dokter']},
Rekam medis Anda masih belum lengkap dengan status:
📄 {row['Status Berkas']}

🗒️ Catatan: {row['Catatan'] or '-'}
{f"\n📌 Tambahan: {catatan_tambahan}" if catatan_tambahan else ''}

Mohon segera dilengkapi. Terima kasih 🙏"""

        st.text_area("📤 Preview Pesan WhatsApp", pesan, height=180)
        st.info("⚠️ Pengiriman WhatsApp belum diaktifkan.\nUntuk kirim otomatis, integrasikan API seperti Twilio atau Wablas.")
else:
    st.success("✅ Semua berkas dokter sudah lengkap.")
