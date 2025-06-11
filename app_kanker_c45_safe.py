import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

st.set_page_config(page_title="Prediksi Kanker Payudara - C4.5", layout="centered")

st.title("🧬 Prediksi Kanker Payudara Menggunakan Algoritma C4.5")

# Upload dataset
uploaded_file = st.file_uploader("📂 Upload Dataset CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Data Rekam Medis")
    st.dataframe(df)

    st.subheader("🧠 Training Model C4.5")

    # Pisahkan fitur dan label
    X = df.drop(columns=["K", "NP"], errors='ignore')  # Hapus label dan nama pasien
    y = df["K"]

    # Bagi data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # C4.5 Decision Tree (entropy-based)
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=5)
    clf.fit(X_train, y_train)

    # Evaluasi
    y_pred = clf.predict(X_test)
    st.text("📈 Akurasi: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
    st.text("📝 Classification Report")
    st.code(classification_report(y_test, y_pred), language="text")

    st.subheader("🌲 Struktur Decision Tree")
    tree_rules = export_text(clf, feature_names=list(X.columns))
    st.code(tree_rules)

    # Simpan model
    joblib.dump(clf, "model_c45.pkl")

    st.subheader("🔍 Prediksi Data Baru")

    # Form input
    input_data = {}
    for col in X.columns:
        input_data[col] = st.number_input(f"{col}", value=0.0)

    if st.button("Prediksi"):
        model = joblib.load("model_c45.pkl")
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        label = "Healthy Control (1)" if prediction == 1 else "Patients (2)"
        st.success(f"Hasil Prediksi: {label}")

        # Unduh hasil prediksi
        hasil_df = input_df.copy()
        hasil_df["Prediksi"] = prediction
        hasil_df.to_csv("hasil_prediksi.csv", index=False)
        with open("hasil_prediksi.csv", "rb") as f:
            st.download_button("⬇️ Download Hasil Prediksi", f, file_name="hasil_prediksi.csv")

else:
    st.info("Silakan upload file CSV terlebih dahulu.")
