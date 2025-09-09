# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 21:02:52 2025

@author: bruno.manzatto
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de Processos", layout="wide")
st.title("📊 Dashboard de Processos")

# 🔗 Excel direto do GitHub
url = "https://raw.githubusercontent.com/brunorestum/processos-raissa/8865afb5a4f900a6322d5559ce2c669bedda799d/processos.xlsx"

# --- Ler Excel ---
df = pd.read_excel(url, engine="openpyxl")

# Mostrar colunas
st.write("📑 Colunas do Excel:")
st.write(df.columns.tolist())

# --- Converter data ---
if "data" in df.columns:
    df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)

# ======================
# Gráfico por Tipo
# ======================
st.subheader("Quantidade de Processos por Tipo")
if "tipo" in df.columns:
    tipo_counts = df["tipo"].dropna().astype(str).value_counts()
    fig1, ax1 = plt.subplots()
    tipo_counts.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Quantidade de Processos")
    ax1.set_xlabel("Tipo")
    st.pyplot(fig1)
else:
    st.warning("❌ Coluna 'tipo' não encontrada.")

# ======================
# Gráfico por Assunto
# ======================
st.subheader("Quantidade de Processos por Assunto")
if "assunto" in df.columns:
    assunto_counts = df["assunto"].dropna().astype(str).value_counts().head(20)
    fig2, ax2 = plt.subplots()
    assunto_counts.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Quantidade de Processos")
    ax2.set_xlabel("Assunto")
    st.pyplot(fig2)
else:
    st.warning("❌ Coluna 'assunto' não encontrada.")

# ======================
# Linha do Tempo
# ======================
st.subheader("📅 Evolução dos Processos por Data")
if "data" in df.columns:
    timeline = (
        df.dropna(subset=["data"])
          .assign(data=df["data"].dt.date)
          .groupby("data")
          .size()
          .sort_index()
    )
    if len(timeline) > 0:
        fig3, ax3 = plt.subplots()
        timeline.plot(kind="line", ax=ax3, marker="o")
        ax3.set_ylabel("Quantidade de Processos")
        ax3.set_xlabel("Data")
        st.pyplot(fig3)
    else:
        st.info("⚠️ Nenhuma data válida encontrada em 'data'.")
else:
    st.warning("❌ Coluna 'data' não encontrada.")
