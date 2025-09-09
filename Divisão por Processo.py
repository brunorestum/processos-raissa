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

# 🔗 CSV direto do GitHub
url = "https://raw.githubusercontent.com/brunorestum/processos-raissa/334e145bb22f3ffd8b205bc0c4e5f880b5e7d0da/processos.csv"

# --- Ler CSV com encoding correto e checar separador ---
try:
    df = pd.read_csv(url, encoding="latin1", sep=",", engine="python")
except Exception:
    df = pd.read_csv(url, encoding="latin1", sep=";", engine="python")

# Mostrar colunas originais
st.write("📑 Colunas originais do CSV:")
st.write(df.columns.tolist())

# --- Normalizar nomes de colunas ---
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("ã", "a")
    .str.replace("â", "a")
    .str.replace("ó", "o")
    .str.replace("ô", "o")
    .str.replace("ç", "c")
)

# --- Forçar renomeio se colunas existirem ---
ren_map = {}
if len(df.columns) >= 2:
    ren_map[df.columns[1]] = "assunto"
if len(df.columns) >= 4:
    ren_map[df.columns[3]] = "data_recebimento"
if len(df.columns) >= 7:
    ren_map[df.columns[6]] = "tipo_assunto"

df = df.rename(columns=ren_map)

# Mostrar colunas finais
st.write("📑 Colunas no CSV após limpeza e renomeio:")
st.write(df.columns.tolist())

# --- Converter data ---
if "data_recebimento" in df.columns:
    df["data_recebimento"] = pd.to_datetime(df["data_recebimento"], errors="coerce", dayfirst=True)

# ======================
# Gráfico por Tipo de Assunto
# ======================
st.subheader("Quantidade de Processos por Tipo de Assunto")
if "tipo_assunto" in df.columns:
    tipo_counts = df["tipo_assunto"].dropna().astype(str).value_counts()
    fig1, ax1 = plt.subplots()
    tipo_counts.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Quantidade de Processos")
    ax1.set_xlabel("Tipo de Assunto")
    st.pyplot(fig1)
else:
    st.warning("❌ Coluna 'tipo_assunto' não encontrada.")

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
st.subheader("📅 Evolução dos Processos por Data de Recebimento")
if "data_recebimento" in df.columns:
    timeline = (
        df.dropna(subset=["data_recebimento"])
          .assign(data=df["data_recebimento"].dt.date)
          .groupby("data")
          .size()
          .sort_index()
    )
    if len(timeline) > 0:
        fig3, ax3 = plt.subplots()
        timeline.plot(kind="line", ax=ax3, marker="o")
        ax3.set_ylabel("Quantidade de Processos")
        ax3.set_xlabel("Data de Recebimento")
        st.pyplot(fig3)
    else:
        st.info("⚠️ Nenhuma data válida encontrada em 'data_recebimento'.")
else:
    st.warning("❌ Coluna 'data_recebimento' não encontrada.")

