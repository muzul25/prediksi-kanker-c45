import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import io

st.set_page_config(page_title="Prediksi Kanker Payudara C4.5", layout="wide")
st.title("🩺 Prediksi Kanker Payudara - Algoritma C4.5 (Decision Tree)")

fitur = ['U', 'B', 'G', 'I', 'H', 'L', 'A', 'R']
target_label = 'K'

# Data training dummy
data_training = pd.DataFrame([
    [34, 23.50, 70, 10.56, 0.74, 8.81, 13.11, 11.79, 1],
    [29, 20.69, 92, 16.64, 4.47, 8.84, 26.72, 4.30, 2],
    [25, 23.12, 91, 4.33, 0.78, 17.94, 23.67, 6.71, 1],
    [24, 21.37, 77, 41.61, 15.29, 9.88, 36.06, 4.50, 2],
    [38, 21.11, 92, 22.03, 1.56, 6.70, 17.95, 4.66, 2],
    [69, 22.85, 92, 3.19, 1.14, 6.83, 20.32, 4.53, 2],
    [60, 32.04, 77, 9.67, 7.84, 6.96, 38.04, 9.61, 2],
    [77, 23.80, 118, 28.68, 2.63, 4.31, 7.78, 8.49, 2],
    [76, 22.00, 97, 10.40, 3.78, 4.47, 5.46, 11.77, 2],
    [76, 23.00, 83, 4.17, 1.10, 17.13, 5.10, 23.03, 2]
], columns=fitur + [target_label])

model = DecisionTreeClassifier(criterion='entropy', random_state=42)
model.fit(data_training[fitur], data_training[target_label])

tab1, tab2 = st.tabs(["🧍 Input Manual", "📁 Upload Excel"])

with tab1:
    st.subheader("Input Data Pasien")
    user_data = {}
    label_dict = {
        'U': "Umur (tahun)", 'B': "BMI (kg/m²)", 'G': "Glukosa (mg/dL)",
        'I': "Insulin (µU/mL)", 'H': "HOMA", 'L': "Leptin (ng/mL)",
        'A': "Adiponektin (µg/mL)", 'R': "Resistin (ng/mL)"
    }
    for f in fitur:
        user_data[f] = st.number_input(label_dict[f], min_value=0.0, format="%.2f")

    if st.button("🔍 Prediksi Manual"):
        input_df = pd.DataFrame([user_data])
        pred = model.predict(input_df)[0]
        hasil = "✅ Healthy Controls (1)" if pred == 1 else "⚠️ Patients (2)"
        st.success(f"Hasil Prediksi: {hasil}")

with tab2:
    st.subheader("Upload File Excel/CSV")
    uploaded_file = st.file_uploader("Unggah file berisi kolom: U, B, G, I, H, L, A, R", type=['xlsx', 'csv'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            if all(col in df.columns for col in fitur):
                prediksi = model.predict(df[fitur])
                df['Prediction'] = prediksi
                df['Prediction_Label'] = df['Prediction'].map({1: 'Healthy', 2: 'Patient'})
                st.success("✅ Prediksi Berhasil!")
                st.dataframe(df)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Prediksi')
                st.download_button(
                    label="💾 Download Hasil Prediksi",
                    data=output.getvalue(),
                    file_name="hasil_prediksi_kanker.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error(f"❌ File tidak memiliki kolom lengkap: {fitur}")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: {e}")
            
