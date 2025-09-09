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
import nltk
from nltk.stem import RSLPStemmer
from collections import Counter

# --- Baixar stopwords ---
nltk.download("stopwords")
from nltk.corpus import stopwords
stopwords_pt = set(stopwords.words("portuguese"))

st.set_page_config(page_title="Análise de Processos", layout="wide")
st.title("📊 Dashboard de Processos")

# Excel do GitHub
url = "https://raw.githubusercontent.com/brunorestum/processos-raissa/8865afb5a4f900a6322d5559ce2c669bedda799d/processos.xlsx"
df = pd.read_excel(url, engine="openpyxl")

# Converter data
if "data" in df.columns:
    df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)

# ======== Gráficos existentes (Tipo, Assunto, Linha do Tempo) ========
st.subheader("📦 Quantidade de Processos por Tipo")
if "tipo" in df.columns:
    tipo_counts = df["tipo"].value_counts().reset_index()
    tipo_counts.columns = ["tipo", "quantidade"]
    fig1 = px.bar(tipo_counts, x="tipo", y="quantidade", text="quantidade", color="tipo")
    st.plotly_chart(fig1, use_container_width=True)

st.subheader("📑 Top 20 Assuntos")
if "assunto" in df.columns:
    assunto_counts = df["assunto"].value_counts().head(20).reset_index()
    assunto_counts.columns = ["assunto", "quantidade"]
    fig2 = px.bar(assunto_counts, x="assunto", y="quantidade", text="quantidade", color="quantidade")
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📅 Evolução dos Processos por Data")
if "data" in df.columns:
    timeline = df.dropna(subset=["data"]).groupby(df["data"].dt.date).size().reset_index(name="quantidade")
    if len(timeline) > 0:
        fig3 = px.line(timeline, x="data", y="quantidade", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

# ======== WordCloud com radical + palavra completa ========
st.subheader("☁️ Palavras mais frequentes nos Assuntos (agrupadas por radical)")

if "assunto" in df.columns:
    stemmer = RSLPStemmer()
    textos = df["assunto"].dropna().astype(str).tolist()

    # Mapeamento: radical -> todas as palavras correspondentes
    radical_map = {}
    for texto in textos:
        for palavra in texto.lower().split():
            palavra = palavra.strip(".,;:!?()[]{}")
            if palavra and palavra not in stopwords_pt:
                rad = stemmer.stem(palavra)
                if rad not in radical_map:
                    radical_map[rad] = []
                radical_map[rad].append(palavra)

    # Para cada radical, pegar a palavra mais frequente correspondente
    palavras_completas = [Counter(pals).most_common(1)[0][0] for pals in radical_map.values()]

    # Criar WordCloud
    texto_wc = " ".join(palavras_completas)
    wordcloud = WordCloud(
        width=800, height=400, background_color="white", colormap="viridis"
    ).generate(texto_wc)

    fig4, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig4)
