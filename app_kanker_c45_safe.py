import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

st.title("Prediksi Kanker Payudara dengan Algoritma ID3")

# Upload Dataset
uploaded_file = st.file_uploader("Upload Dataset CSV", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(data)

    if 'K' not in data.columns:
        st.error("Kolom target 'K' (klasifikasi 1/2) tidak ditemukan.")
    else:
        # Pisahkan fitur dan target
        X = data.drop(columns=['K'])
        y = data['K']

        # Split untuk validasi internal (opsional)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Buat model ID3 (DecisionTreeClassifier dengan entropy)
        model = DecisionTreeClassifier(criterion='entropy')
        model.fit(X_train, y_train)

        # Tampilkan pohon keputusan
        st.subheader("Struktur Pohon Keputusan")
        tree_rules = export_text(model, feature_names=list(X.columns))
        st.code(tree_rules)

        # Evaluasi model
        st.subheader("Evaluasi Model")
        y_pred = model.predict(X_test)
        st.text(classification_report(y_test, y_pred))

        # Prediksi data baru
        st.subheader("Prediksi Data Baru")
        input_data = {}
        for col in X.columns:
            input_data[col] = st.number_input(f"Masukkan nilai untuk {col}", value=0.0)

        if st.button("Prediksi"):
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
            label = "Healthy Controls (1)" if prediction == 1 else "Patients (2)"
            st.success(f"Hasil Prediksi: {label}")

        # Export hasil prediksi
        st.subheader("Export Hasil Prediksi")
        if st.button("Export CSV"):
            data['Prediksi'] = model.predict(X)
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("Download hasil.csv", csv, "hasil_prediksi.csv", "text/csv")
