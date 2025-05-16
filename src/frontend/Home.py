import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("📊 Relatórios Inteligentes - IPEA")

# Dados financeiros
dados = requests.get("http://localhost:8000/api/dados").json()
df = pd.DataFrame(dados)

fig = px.line(df, x="ano", y="valor", title="Gastos por Ano")
st.plotly_chart(fig)

# Resumo automático
resumo = requests.get("http://localhost:8000/api/resumo").json()
st.subheader("Resumo Automático")
st.text(resumo["resumo"])

# Alertas
alertas = requests.get("http://localhost:8000/api/alertas").json()
st.subheader("Alertas Financeiros")
for alerta in alertas:
    st.warning(alerta)
