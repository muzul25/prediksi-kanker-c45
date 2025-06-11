import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import base64

st.set_page_config(page_title="Prediksi Kanker Payudara - C4.5", layout="wide")
st.title("🎗️ Prediksi Kanker Payudara dengan C4.5")

uploaded_file = st.file_uploader("📂 Upload Dataset CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data yang Diupload")
    st.write(df)

    if 'K' not in df.columns:
        st.error("Kolom label 'K' (klasifikasi) tidak ditemukan.")
    else:
        X = df.drop(columns=['K', 'NP'], errors='ignore')  # NP = Nama Pasien jika ada
        y = df['K']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model
        model = DecisionTreeClassifier(criterion="entropy", random_state=42)
        model.fit(X_train, y_train)

        st.subheader("🌲 Pohon Keputusan (C4.5 Style)")
        st.text(export_text(model, feature_names=list(X.columns)))

        # Evaluasi
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        st.subheader("📊 Evaluasi Model")
        st.json(report)

        # Prediksi Data Baru
        st.subheader("🧪 Prediksi Data Baru")
        input_data = {}
        for col in X.columns:
            input_data[col] = st.number_input(f"{col}", value=0.0)
        
        if st.button("Prediksi"):
            df_new = pd.DataFrame([input_data])
            prediction = model.predict(df_new)[0]
            st.success(f"Hasil Prediksi: {'Sehat (1)' if prediction == 1 else 'Pasien (2)'}")

        # Simpan hasil ke Excel
        if st.button("📤 Ekspor Hasil Prediksi ke Excel"):
            df['Prediksi'] = model.predict(X)
            excel_file = "hasil_prediksi.xlsx"
            df.to_excel(excel_file, index=False)

            with open(excel_file, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{excel_file}">⬇️ Unduh hasil_prediksi.xlsx</a>'
                st.markdown(href, unsafe_allow_html=True)
