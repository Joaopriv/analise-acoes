# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run app.py
```

## Architecture

Single-file Streamlit app (`app.py`) that fetches and visualizes Brazilian stock data for 2025.

**Data layer:** `carregar_dados()` uses `yfinance` to download OHLCV data for PETR4.SA, ITUB4.SA, and VALE3.SA. Results are cached with `@st.cache_data(ttl=3600)` to avoid repeated API calls.

**Presentation layer:** Four tabs, each rendering a Plotly chart:
- Tab 1 — Normalized comparison (base 100 from Jan/2025)
- Tab 2 — Closing price per stock (3-row subplot)
- Tab 3 — Cumulative percentage return
- Tab 4 — Daily trading volume (3-row bar subplot)

The `TICKERS` dict maps display names to Yahoo Finance symbols (`.SA` suffix = B3 exchange). The `CORES` dict maps the same names to brand colors used consistently across all charts.

## GitHub Repository

Repositório: https://github.com/Joaopriv/analise-acoes

**Sincronização automática:** toda vez que Claude Code edita ou cria um arquivo, um hook `PostToolUse` faz automaticamente `git add -A`, `git commit` e `git push` para o repositório remoto. A configuração está em `.claude/settings.json`.

Para forçar um push manual:
```bash
git add -A && git commit -m "sua mensagem" && git push
```
