import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

st.title("🧬 Prediksi Kanker Payudara - Algoritma ID3")

st.markdown("""
**Atribut yang digunakan:**
- U = Umur (Tahun)
- B = BMI (Kg/M2)
- G = Glucose (mg/dL)
- I = Insulin (µU/mL)
- H = HOMA
- L = Leptin (ng/mL)
- A = Adiponectin (µg/mL)
- R = Resistin (ng/mL)
- K = Klasifikasi (1 = Sehat, 2 = Pasien)
""")

uploaded_file = st.file_uploader("📂 Upload dataset CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    required_cols = ['U', 'B', 'G', 'I', 'H', 'L', 'A', 'R', 'K']
    if not all(col in df.columns for col in required_cols):
        st.error("⚠️ Dataset harus memiliki kolom: " + ", ".join(required_cols))
    else:
        X = df.drop(columns=['K'])
        y = df['K']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = DecisionTreeClassifier(criterion="entropy", random_state=0)
        model.fit(X_train, y_train)

        st.subheader("🌳 Struktur Pohon Keputusan (ID3)")
        rules = export_text(model, feature_names=list(X.columns))
        st.code(rules)

        st.subheader("📈 Evaluasi Model")
        y_pred = model.predict(X_test)
        st.text(classification_report(y_test, y_pred))

        st.subheader("🧪 Prediksi Data Baru")
        input_data = {}
        for col in X.columns:
            input_data[col] = st.number_input(f"{col}", value=0.0)

        if st.button("🔍 Prediksi"):
            input_df = pd.DataFrame([input_data])
            hasil = model.predict(input_df)[0]
            st.success(f"Hasil prediksi: {'Healthy Controls (1)' if hasil == 1 else 'Patients (2)'}")

        st.subheader("⬇️ Export Hasil Prediksi")
        if st.button("Export CSV"):
            df['Prediksi'] = model.predict(X)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download hasil_prediksi.csv", csv, "hasil_prediksi.csv", "text/csv")
