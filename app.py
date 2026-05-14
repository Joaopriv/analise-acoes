import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Análise de Ações 2025",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Análise de Ações Brasileiras — 2025")
st.markdown("Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3)")

TICKERS = {
    "Petrobras (PETR4)": "PETR4.SA",
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
}

CORES = {
    "Petrobras (PETR4)": "#009c3b",
    "Itaú (ITUB4)": "#003d99",
    "Vale (VALE3)": "#c8a951",
}


@st.cache_data(ttl=3600)
def carregar_dados():
    dados = {}
    for nome, ticker in TICKERS.items():
        df = yf.download(ticker, start="2025-01-01", end="2025-12-31", progress=False, auto_adjust=True)
        df.columns = df.columns.get_level_values(0)
        dados[nome] = df
    return dados


with st.spinner("Carregando dados do mercado..."):
    dados = carregar_dados()

# Métricas de resumo
st.subheader("Resumo")
cols = st.columns(3)
for i, (nome, df) in enumerate(dados.items()):
    if df.empty:
        cols[i].metric(nome, "Sem dados")
        continue
    preco_atual = float(df["Close"].iloc[-1])
    preco_inicio = float(df["Close"].iloc[0])
    retorno = ((preco_atual - preco_inicio) / preco_inicio) * 100
    variacao_dia = float(df["Close"].iloc[-1]) - float(df["Close"].iloc[-2]) if len(df) > 1 else 0
    variacao_dia_pct = (variacao_dia / float(df["Close"].iloc[-2])) * 100 if len(df) > 1 else 0
    cols[i].metric(
        nome,
        f"R$ {preco_atual:.2f}",
        f"{variacao_dia_pct:+.2f}% hoje · {retorno:+.2f}% em 2025",
    )

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Comparação",
    "📉 Evolução do Preço",
    "💹 Retorno Percentual",
    "📦 Volume Negociado",
])

# --- Tab 1: Comparação normalizada ---
with tab1:
    st.markdown("### Comparação entre as 3 ações (base 100 em jan/2025)")
    fig = go.Figure()
    for nome, df in dados.items():
        if df.empty:
            continue
        normalizado = (df["Close"] / float(df["Close"].iloc[0])) * 100
        fig.add_trace(go.Scatter(
            x=df.index,
            y=normalizado,
            name=nome,
            line=dict(color=CORES[nome], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>Base 100: %{y:.2f}<extra>" + nome + "</extra>",
        ))
    fig.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        yaxis_title="Valor (base 100)",
        xaxis_title="Data",
        hovermode="x unified",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: Evolução do preço ---
with tab2:
    st.markdown("### Evolução do preço de fechamento")
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                        subplot_titles=list(TICKERS.keys()))
    for i, (nome, df) in enumerate(dados.items(), start=1):
        if df.empty:
            continue
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            name=nome,
            line=dict(color=CORES[nome], width=2),
            showlegend=False,
            hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + nome + "</extra>",
        ), row=i, col=1)
        fig.update_yaxes(title_text="R$", row=i, col=1)
    fig.update_layout(height=700, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 3: Retorno percentual ---
with tab3:
    st.markdown("### Retorno percentual acumulado em 2025")
    fig = go.Figure()
    for nome, df in dados.items():
        if df.empty:
            continue
        retorno = ((df["Close"] - float(df["Close"].iloc[0])) / float(df["Close"].iloc[0])) * 100
        fig.add_trace(go.Scatter(
            x=df.index,
            y=retorno,
            name=nome,
            line=dict(color=CORES[nome], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>Retorno: %{y:.2f}%<extra>" + nome + "</extra>",
        ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        yaxis_title="Retorno (%)",
        xaxis_title="Data",
        hovermode="x unified",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 4: Volume negociado ---
with tab4:
    st.markdown("### Volume diário negociado")
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                        subplot_titles=list(TICKERS.keys()))
    for i, (nome, df) in enumerate(dados.items(), start=1):
        if df.empty:
            continue
        fig.add_trace(go.Bar(
            x=df.index,
            y=df["Volume"],
            name=nome,
            marker_color=CORES[nome],
            showlegend=False,
            hovertemplate="%{x|%d/%m/%Y}<br>Volume: %{y:,.0f}<extra>" + nome + "</extra>",
        ), row=i, col=1)
        fig.update_yaxes(title_text="Volume", row=i, col=1)
    fig.update_layout(height=700, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
