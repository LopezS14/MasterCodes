import streamlit as st

# Dividir en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.title("Hope_Beta 001")
    st.write("Te doy la bienvenida, estoy aquí para ayudarte.")
    user_input = st.text_input("Estoy para ti, ¿qué necesitas?")
    if st.button("Analízame"):
        st.write("Procesando tu estado emocional...")

with col2:
    st.subheader("Ejecutando Análisis")
    st.image("captura_emocion.png", caption="Detección de emoción")
