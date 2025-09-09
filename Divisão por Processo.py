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

# Substitua pelo link RAW do GitHub
url = "https://raw.githubusercontent.com/brunorestum/processos-raissa/334e145bb22f3ffd8b205bc0c4e5f880b5e7d0da/processos.csv"
df = pd.read_csv(url)


# --- Leitura robusta do CSV (tenta detectar separador; fallback para ; e ,) ---
def read_csv_resilient(src_url: str) -> pd.DataFrame:
    # 1) tenta autodetectar separador
    try:
        df_try = pd.read_csv(src_url, sep=None, engine="python", encoding="utf-8")
        if df_try.shape[1] > 1:
            return df_try
    except Exception:
        pass

    # 2) tenta ; (muito comum no Brasil)
    try:
        df_try = pd.read_csv(src_url, sep=";", encoding="latin1")
        if df_try.shape[1] > 1:
            return df_try
    except Exception:
        pass

    # 3) tenta , com latin1
    try:
        df_try = pd.read_csv(src_url, sep=",", encoding="latin1")
        return df_try
    except Exception as e:
        st.error("❌ Não foi possível ler o CSV pela URL. Verifique se é um link RAW público.")
        st.stop()

df = read_csv_resilient(url)

# --- Renomear colunas por posição ---
num_cols = len(df.columns)
ren_map = {}
if num_cols >= 2: ren_map[df.columns[1]] = "assunto"            # 2ª coluna (idx 1)
if num_cols >= 4: ren_map[df.columns[3]] = "data_recebimento"   # 4ª coluna (idx 3)
if num_cols >= 7: ren_map[df.columns[6]] = "tipo_assunto"       # 7ª coluna (idx 6)
df = df.rename(columns=ren_map)

# Padroniza nomes (sem espaços extras e tudo minúsculo — exceto as que já definimos acima)
df.columns = [c.strip() for c in df.columns]
# Garantir que as três existam após renomear (caso o CSV mude de ordem/nome)
tem_assunto = "assunto" in df.columns
tem_tipo_assunto = "tipo_assunto" in df.columns
tem_data = "data_recebimento" in df.columns

col1, col2 = st.columns([2, 1])
with col2:
    st.write("📑 Colunas detectadas:")
    st.write(df.columns.tolist())

# --- Converter data_recebimento para datetime (se existir) ---
if tem_data:
    df["data_recebimento"] = pd.to_datetime(df["data_recebimento"], errors="coerce", dayfirst=True)

# ======================
# Gráfico por Tipo de Assunto
# ======================
st.subheader("Quantidade de Processos por Tipo de Assunto")
if tem_tipo_assunto:
    tipo_counts = df["tipo_assunto"].dropna().astype(str).value_counts()
    fig1, ax1 = plt.subplots()
    tipo_counts.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Quantidade de Processos")
    ax1.set_xlabel("Tipo de Assunto")
    ax1.set_title("Processos por Tipo de Assunto")
    st.pyplot(fig1)
else:
    st.warning("❌ Coluna 'tipo_assunto' não encontrada após o renomeio (7ª coluna).")

# ======================
# Gráfico por Assunto
# ======================
st.subheader("Quantidade de Processos por Assunto")
if tem_assunto:
    # Limita aos Top N para evitar poluição visual
    top_n = st.slider("Top N assuntos", min_value=5, max_value=50, value=20, step=5)
    assunto_counts = df["assunto"].dropna().astype(str).value_counts().head(top_n)
    fig2, ax2 = plt.subplots()
    assunto_counts.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Quantidade de Processos")
    ax2.set_xlabel("Assunto")
    ax2.set_title(f"Top {top_n} Assuntos")
    st.pyplot(fig2)
else:
    st.warning("❌ Coluna 'assunto' não encontrada após o renomeio (2ª coluna).")

# ======================
# Linha do Tempo por Data de Recebimento
# ======================
st.subheader("📅 Evolução dos Processos por Data de Recebimento")
if tem_data:
    timeline = (
        df.dropna(subset=["data_recebimento"])
          .assign(data=df["data_recebimento"].dt.date)
          .groupby("data")
          .size()
          .sort_index()
    )
    if len(timeline) == 0:
        st.info("Sem datas válidas em 'data_recebimento' para montar a linha do tempo.")
    else:
        fig3, ax3 = plt.subplots()
        timeline.plot(kind="line", ax=ax3, marker="o")
        ax3.set_ylabel("Quantidade de Processos")
        ax3.set_xlabel("Data de Recebimento")
        ax3.set_title("Evolução Diária de Processos")
        st.pyplot(fig3)
else:
    st.warning("❌ Coluna 'data_recebimento' não encontrada após o renomeio (4ª coluna).")
