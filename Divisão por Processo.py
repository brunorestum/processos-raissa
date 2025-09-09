# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 21:02:52 2025

@author: bruno.manzatto
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de Processos", layout="wide")
st.title("📊 Dashboard de Processos")

# 🔗 Excel direto do GitHub
url = "https://raw.githubusercontent.com/brunorestum/processos-raissa/8865afb5a4f900a6322d5559ce2c669bedda799d/processos.xlsx"
df = pd.read_excel(url, engine="openpyxl")

# Converter data
if "data" in df.columns:
    df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)

# ======================
# Gráfico por Tipo (Plotly)
# ======================
st.subheader("📦 Quantidade de Processos por Tipo")
if "tipo" in df.columns:
    tipo_counts = df["tipo"].value_counts().reset_index()
    tipo_counts.columns = ["tipo", "quantidade"]
    fig1 = px.bar(
        tipo_counts,
        x="tipo",
        y="quantidade",
        text="quantidade",
        color="tipo",
        title="Quantidade de Processos por Tipo",
    )
    st.plotly_chart(fig1, use_container_width=True)

# ======================
# Gráfico por Assunto (Plotly)
# ======================
st.subheader("📑 Top 20 Assuntos")
if "assunto" in df.columns:
    assunto_counts = df["assunto"].value_counts().head(20).reset_index()
    assunto_counts.columns = ["assunto", "quantidade"]
    fig2 = px.bar(
        assunto_counts,
        x="assunto",
        y="quantidade",
        text="quantidade",
        color="quantidade",
        title="Top 20 Assuntos",
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

# ======================
# Linha do Tempo (Plotly)
# ======================
st.subheader("📅 Evolução dos Processos por Data")
if "data" in df.columns:
    timeline = df.dropna(subset=["data"]).groupby(df["data"].dt.date).size().reset_index(name="quantidade")
    if len(timeline) > 0:
        fig3 = px.line(
            timeline,
            x="data",
            y="quantidade",
            markers=True,
            title="Evolução dos Processos ao longo do tempo"
        )
        st.plotly_chart(fig3, use_container_width=True)

# ======================
# WordCloud com RADICAIS MANUAIS
# ======================
st.subheader("☁️ Radicais mais frequentes nos Assuntos")

if "assunto" in df.columns:
    stopwords_pt = set([
        "de", "do", "da", "em", "para", "com", "sem",
        "a", "o", "e", "os", "as", "um", "uma",
        "por", "na", "no", "nas", "nos", "se"
    ])

    # Função simples para extrair radical
    def extrair_radical(palavra):
        sufixos = ["mente", "ções", "ção", "s", "es", "e", "a", "o"]
        for suf in sufixos:
            if palavra.endswith(suf) and len(palavra) > len(suf) + 2:
                return palavra[:-len(suf)]
        return palavra

    # Extrair radicais
    radicais = []
    for texto in df["assunto"].dropna().astype(str):
        for palavra in texto.lower().split():
            palavra = palavra.strip(".,;:!?()[]{}")
            if palavra and palavra not in stopwords_pt:
                radicais.append(extrair_radical(palavra))

    # Criar WordCloud
    texto_wc = " ".join(radicais)
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="viridis"
    ).generate(texto_wc)

    fig4, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig4)
