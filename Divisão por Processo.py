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

# 🔗 CSV direto do GitHub (RAW link público)
url = "https://raw.githubusercontent.com/brunorestum/processos-raissa/334e145bb22f3ffd8b205bc0c4e5f880b5e7d0da/processos.csv"

# --- Leitura robusta do CSV ---
def read_csv_resilient(src_url: str) -> pd.DataFrame:
    try:
        df_try = pd.read_csv(src_url, sep=None, engine="python", encoding="utf-8")
        if df_try.shape[1] > 1:
            return df_try
    except Exception:
        pass
    try:
        df_try = pd.read_csv(src_url, sep=";", encoding="latin1")
        if df_try.shape[1] > 1:
            return df_try
    except Exception:
        pass
    try:
        df_try = pd.read_csv(src_url, sep=",", encoding="latin1")
        return df_try
    except Exception:
        st.error("❌ Não foi possível ler o CSV pela URL. Verifique o link RAW.")
        st.stop()

df = read_csv_resilient(url)

# --- Renomear colunas por posição ---
num_cols = len(df.columns)
ren_map = {}
if num_cols >= 2: ren_map[df.columns[1]] = "assunto"
if num_cols >= 4: ren_map[df.columns[3]] = "data_recebimento"
if num_cols >= 7: ren_map[df.columns[6]] = "tipo_assunto"
df = df.rename(columns=ren_map)

# Mostrar colunas detectadas
st.write("📑 Colunas no CSV após renomeio:")
st.write(df.columns.tolist())

# Converter datas
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
    st.warning("❌ Coluna 'tipo_assunto' não encontrada (7ª coluna).")

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
    st.warning("❌ Coluna 'assunto' não encontrada (2ª coluna).")

# ======================
# Linha do Tempo por Data de Recebimento
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
    st.warning("❌ Coluna 'data_recebimento' não encontrada (4ª coluna).")
