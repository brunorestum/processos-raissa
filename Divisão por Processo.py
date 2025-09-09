# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 21:02:52 2025

@author: bruno.manzatto
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de Processos", layout="wide")

# Substitua pelo link RAW do GitHub
url = "https://raw.githubusercontent.com/brunorestum/processos-raissa/334e145bb22f3ffd8b205bc0c4e5f880b5e7d0da/processos.csv"
df = pd.read_csv(url)

# Mostrar colunas disponíveis
st.write("📑 Colunas no CSV:")
st.write(df.columns.tolist())

# Padronizar nomes (remover espaços extras e deixar tudo minúsculo)
df.columns = df.columns.str.strip().str.lower()

# Agora tentamos usar os nomes padronizados
if "data de recebimento" in df.columns:
    df["data de recebimento"] = pd.to_datetime(df["data de recebimento"], errors="coerce")

st.title("📊 Dashboard de Processos")

# ======================
# Gráfico por Tipo Assunto
# ======================
if "tipo assunto" in df.columns:
    st.subheader("Quantidade de Processos por Tipo de Assunto")
    tipo_counts = df["tipo assunto"].value_counts()

    fig1, ax1 = plt.subplots()
    tipo_counts.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Quantidade de Processos")
    ax1.set_xlabel("Tipo de Assunto")
    st.pyplot(fig1)
else:
    st.warning("❌ Coluna 'tipo assunto' não encontrada no CSV.")

# ======================
# Gráfico por Assunto
# ======================
if "assunto" in df.columns:
    st.subheader("Quantidade de Processos por Assunto")
    assunto_counts = df["assunto"].value_counts().head(20)

    fig2, ax2 = plt.subplots()
    assunto_counts.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Quantidade de Processos")
    ax2.set_xlabel("Assunto")
    st.pyplot(fig2)
else:
    st.warning("❌ Coluna 'assunto' não encontrada no CSV.")

# ======================
# Linha do Tempo por Data de Recebimento
# ======================
if "data de recebimento" in df.columns:
    st.subheader("📅 Evolução dos Processos por Data de Recebimento")
    timeline = df.groupby("data de recebimento").size()

    fig3, ax3 = plt.subplots()
    timeline.plot(kind="line", ax=ax3, marker="o")
    ax3.set_ylabel("Quantidade de Processos")
    ax3.set_xlabel("Data de Recebimento")
    st.pyplot(fig3)
else:
    st.warning("❌ Coluna 'data de recebimento' não encontrada no CSV.")
