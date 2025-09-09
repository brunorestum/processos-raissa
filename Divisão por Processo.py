# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 21:02:52 2025

@author: bruno.manzatto
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial da página
st.set_page_config(page_title="Análise de Processos", layout="wide")

# Carregar CSV
df = pd.read_csv("processos.csv")

# Garantir que a coluna de data esteja em formato datetime
if "data de recebimento" in df.columns:
    df["data de recebimento"] = pd.to_datetime(df["data de recebimento"], errors="coerce")

st.title("📊 Dashboard de Processos")

# ======================
# Gráfico por Tipo Assunto
# ======================
st.subheader("Quantidade de Processos por Tipo de Assunto")
tipo_counts = df["tipo assunto"].value_counts()

fig1, ax1 = plt.subplots()
tipo_counts.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Quantidade de Processos")
ax1.set_xlabel("Tipo de Assunto")
st.pyplot(fig1)

# ======================
# Gráfico por Assunto
# ======================
st.subheader("Quantidade de Processos por Assunto")
assunto_counts = df["assunto"].value_counts().head(20)  # pega só os 20 mais comuns para não poluir

fig2, ax2 = plt.subplots()
assunto_counts.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Quantidade de Processos")
ax2.set_xlabel("Assunto")
st.pyplot(fig2)

# ======================
# Linha do Tempo por Data de Recebimento
# ======================
st.subheader("📅 Evolução dos Processos por Data de Recebimento")

if "data de recebimento" in df.columns:
    timeline = df.groupby("data de recebimento").size()

    fig3, ax3 = plt.subplots()
    timeline.plot(kind="line", ax=ax3, marker="o")
    ax3.set_ylabel("Quantidade de Processos")
    ax3.set_xlabel("Data de Recebimento")
    st.pyplot(fig3)
else:
    st.warning("A coluna 'data de recebimento' não foi encontrada no CSV.")
