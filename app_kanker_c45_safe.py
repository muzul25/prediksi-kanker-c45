import streamlit as st
import pandas as pd
from urllib.parse import quote
from datetime import datetime

st.set_page_config("📲 Follow-Up Berkas Dokter", layout="wide")

st.title("🩺 Sistem Follow-Up Berkas Dokter")

# Inisialisasi data dokter
if "dokter_df" not in st.session_state:
    st.session_state.dokter_df = pd.DataFrame({
        "Nama Dokter": ["dr. Andi", "dr. Budi", "dr. Clara"],
        "Nomor WA": ["6281234567890", "6281234500001", "6281212345678"],
        "Status Berkas": ["❌ Belum Lengkap", "✅ Lengkap", "❌ Belum Lengkap"],
        "Catatan": ["Belum upload hasil lab", "", "Form anamnesa belum dikirim"]
    })

# Inisialisasi riwayat follow-up
if "riwayat_df" not in st.session_state:
    st.session_state.riwayat_df = pd.DataFrame(columns=["Waktu", "Nama Dokter", "Pesan"])

# --- FORM TAMBAH DOKTER
with st.expander("➕ Tambah Dokter Baru"):
    with st.form("form_dokter"):
        nama = st.text_input("Nama Dokter")
        nomor = st.text_input("Nomor WA (cth: 6281234567890)")
        status = st.selectbox("Status Berkas", ["❌ Belum Lengkap", "✅ Lengkap"])
        catatan = st.text_area("Catatan Berkas")
        submit = st.form_submit_button("Tambah ke Daftar")

        if submit:
            new_row = pd.DataFrame({
                "Nama Dokter": [nama],
                "Nomor WA": [nomor],
                "Status Berkas": [status],
                "Catatan": [catatan]
            })
            st.session_state.dokter_df = pd.concat([st.session_state.dokter_df, new_row], ignore_index=True)
            st.success(f"✅ Dokter {nama} ditambahkan!")

# --- TABEL & EXPORT CSV
st.subheader("📋 Daftar Dokter")
st.dataframe(st.session_state.dokter_df, use_container_width=True)

csv = st.session_state.dokter_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV Dokter", data=csv, file_name="daftar_dokter.csv", mime="text/csv")

# --- PILIH DOKTER UNTUK FOLLOW-UP
st.subheader("📤 Follow-Up WhatsApp")
df_filter = st.session_state.dokter_df[st.session_state.dokter_df["Status Berkas"] == "❌ Belum Lengkap"]

if len(df_filter) == 0:
    st.info("Semua dokter sudah melengkapi berkas 🙌")
else:
    dokter_terpilih = st.selectbox("Pilih Dokter yang Belum Lengkap", df_filter["Nama Dokter"])
    catatan_tambahan = st.text_area("📝 Tambahkan Catatan Tambahan (Opsional)")

    info = df_filter[df_filter["Nama Dokter"] == dokter_terpilih].iloc[0]
    nomor = info["Nomor WA"]
    catatan = info["Catatan"]

    # Buat isi pesan
    pesan = f"Halo {dokter_terpilih}, mohon segera melengkapi berkas pasien.\n\nCatatan: {catatan}"
    if catatan_tambahan:
        pesan += f"\nTambahan: {catatan_tambahan}"
    url = f"https://wa.me/{nomor}?text={quote(pesan)}"

    # Tampilkan tautan WA
    st.markdown(f"👉 [📲 Kirim WhatsApp ke {dokter_terpilih}]({url})", unsafe_allow_html=True)

    if st.button("📌 Simpan ke Riwayat Follow-Up"):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame([[waktu, dokter_terpilih, pesan]], columns=["Waktu", "Nama Dokter", "Pesan"])
        st.session_state.riwayat_df = pd.concat([st.session_state.riwayat_df, new_row], ignore_index=True)
        st.success("✅ Riwayat follow-up disimpan.")

# --- TAMPILKAN RIWAYAT
st.subheader("🕘 Riwayat Follow-Up")
if st.session_state.riwayat_df.empty:
    st.info("Belum ada follow-up dilakukan.")
else:
    st.dataframe(st.session_state.riwayat_df, use_container_width=True)
    riwayat_csv = st.session_state.riwayat_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Riwayat Follow-Up", data=riwayat_csv, file_name="riwayat_followup.csv", mime="text/csv")
