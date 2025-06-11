import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

st.set_page_config(page_title="Prediksi Kanker Payudara", layout="centered")
st.title("🧬 Prediksi Kanker Payudara dengan Algoritma ID3 (Decision Tree)")
st.markdown("Gunakan upload dataset **ATAU** input manual pasien baru.")

# ----------- DATASET SECTION ----------------
uploaded_file = st.file_uploader("📂 Upload Dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    required_cols = ['U', 'B', 'G', 'I', 'H', 'L', 'A', 'R', 'K']
    if not all(col in df.columns for col in required_cols):
        st.error("Dataset harus punya kolom: " + ", ".join(required_cols))
    else:
        X = df.drop(columns=['K'])
        y = df['K']
        model = DecisionTreeClassifier(criterion="entropy")
        model.fit(X, y)

        # Show tree
        st.subheader("🌳 Struktur Pohon Keputusan")
        st.code(export_text(model, feature_names=X.columns.to_list()))

        # Form manual input
        st.subheader("🧾 Form Manual Input Pasien Baru")
        col1, col2 = st.columns(2)
        with col1:
            umur = st.number_input("Umur (U)", min_value=1, max_value=120, step=1)
            bmi = st.number_input("BMI (B)", format="%.2f")
            glukosa = st.number_input("Glukosa (G)", format="%.2f")
            insulin = st.number_input("Insulin (I)", format="%.2f")
        with col2:
            homa = st.number_input("HOMA (H)", format="%.2f")
            leptin = st.number_input("Leptin (L)", format="%.2f")
            adiponectin = st.number_input("Adiponectin (A)", format="%.2f")
            resistin = st.number_input("Resistin (R)", format="%.2f")

        if st.button("🔍 Prediksi"):
            input_df = pd.DataFrame([{
                'U': umur,
                'B': bmi,
                'G': glukosa,
                'I': insulin,
                'H': homa,
                'L': leptin,
                'A': adiponectin,
                'R': resistin
            }])
            hasil = model.predict(input_df)[0]
            label = "✅ Sehat (Healthy Controls)" if hasil == 1 else "⚠️ Terindikasi Pasien (Patients)"
            st.success(f"Hasil Prediksi: **{label} (K = {hasil})**")

        st.subheader("⬇️ Export Prediksi dari Dataset")
        if st.button("Export CSV"):
            df['Prediksi'] = model.predict(X)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download hasil_prediksi.csv", csv, "hasil_prediksi.csv", "text/csv")
else:
    st.info("Silakan upload dataset terlebih dahulu untuk memulai prediksi dan input manual.")
