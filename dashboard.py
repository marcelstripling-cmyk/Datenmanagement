# dashboard.py
# Empfohlene Installation:
# pip install streamlit pandas plotly

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Preis-Analyse Dashboard", layout="wide")

st.title("Preis- & Ausreißer-Analyse Dashboard")
st.markdown("Lade deine CSV hoch und speichere interessante Ansichten innerhalb des Dashboards.")

# ── Session State ────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = None

if "saved_views" not in st.session_state:
    st.session_state.saved_views = []   # Liste von Dictionaries

if "selected_view" not in st.session_state:
    st.session_state.selected_view = None

# ── Datei-Upload ─────────────────────────────────────────────────
uploaded_file = st.file_uploader("CSV-Datei hochladen", type=["csv"])

if uploaded_file is not None and st.session_state.df is None:
    try:
        # Encoding-Versuche
        df = pd.read_csv(uploaded_file, sep=None, engine="python", on_bad_lines="warn")
        df = df.dropna(how="all").dropna(axis=1, how="all")
        
        st.session_state.df = df
        
        # Spaltenvorschläge vorbereiten
        num_cols = df.select_dtypes(include="number").columns.tolist()
        possible_years = [c for c in df.columns if any(k in str(c).lower() for k in ["jahr","year","date","zeit"])]
        possible_prices = [c for c in num_cols if any(k in str(c).lower() for k in ["preis","price","kosten","eur","€"])]
        
        st.session_state.default_year = possible_years[0] if possible_years else None
        st.session_state.default_price = possible_prices[0] if possible_prices else None
        
        st.success(f"Daten geladen: {len(df):,} Zeilen, {len(df.columns)} Spalten")
    except Exception as e:
        st.error(f"Fehler beim Einlesen:\n{str(e)}")

# ── Wenn Daten vorhanden ─────────────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df
    
    # ── Spaltenauswahl ───────────────────────────────────────────
    col1, col2, col3 = st.columns([2,2,1.5])
    
    with col1:
        x_col = st.selectbox(
            "X-Achse (meist Jahr / Zeit)",
            options = df.columns.tolist(),
            index = df.columns.get_loc(st.session_state.default_year) if st.session_state.default_year else 0,
            key = "x_col"
        )
    
    with col2:
        y_col = st.selectbox(
            "Y-Achse (Preis)",
            options = df.select_dtypes(include="number").columns.tolist(),
            index = df.columns.get_loc(st.session_state.default_price) if st.session_state.default_price in df.select_dtypes(include="number").columns else 0,
            key = "y_col"
        )
    
    with col3:
        group_col = st.selectbox(
            "Gruppieren / Farbe nach (optional)",
            options = ["Keine"] + df.columns.tolist(),
            index = 0,
            key = "group_col"
        )
    
    st.markdown("---")
    
    # ── Die drei vorgegebenen Analysen ────────────────────────────
    analyses = [
        {
            "name": "1. Preisspanne teuer ↔ günstig",
            "desc": "Min und Max Preis pro Jahr (Schwankungsband)",
            "type": "range"
        },
        {
            "name": "2. Median vs. Durchschnitt",
            "desc": "Vergleich Median und arithmetisches Mittel pro Jahr",
            "type": "median_mean"
        },
        {
            "name": "3. Positive & negative Ausreißer",
            "desc": "Ausreißer nach IQR-Methode (1.5 × IQR)",
            "type": "outliers"
        }
    ]
    
    cols = st.columns(3)
    
    for idx, analysis in enumerate(analyses):
        with cols[idx]:
            st.subheader(analysis["name"])
            st.caption(analysis["desc"])
            
            fig = None
            
            if analysis["type"] == "range":
                grouped = df.groupby(x_col)[y_col].agg(['min','max']).reset_index()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=grouped[x_col], y=grouped['max'], name="Max (teuer)", line=dict(color='darkred')))
                fig.add_trace(go.Scatter(x=grouped[x_col], y=grouped['min'], name="Min (günstig)", line=dict(color='darkgreen')))
                fig.add_trace(go.Scatter(x=grouped[x_col], y=grouped['max'], fill='tonexty', fillcolor='rgba(220,20,60,0.12)', line=dict(color='rgba(255,255,255,0)')))
                fig.update_layout(
                    title="Preisspanne pro Zeitraum",
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    hovermode="x unified"
                )
            
            elif analysis["type"] == "median_mean":
                grouped = df.groupby(x_col)[y_col].agg(['mean','median']).reset_index()
                fig = px.line(
                    grouped.melt(id_vars=x_col, value_vars=['mean','median']),
                    x=x_col, y="value", color="variable",
                    title="Durchschnitt vs. Median pro Zeitraum",
                    labels={"value": y_col, "variable": "Maß"}
                )
            
            elif analysis["type"] == "outliers":
                def flag_outliers(g):
                    Q1 = g[y_col].quantile(0.25)
                    Q3 = g[y_col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    g['Typ'] = 'normal'
                    g.loc[g[y_col] < lower, 'Typ'] = 'negativer Ausreißer'
                    g.loc[g[y_col] > upper, 'Typ'] = 'positiver Ausreißer'
                    return g
                
                df_out = df.groupby(x_col, group_keys=False).apply(flag_outliers)
                outliers = df_out[df_out['Typ'] != 'normal']
                
                if len(outliers) > 0:
                    fig = px.scatter(
                        outliers,
                        x=x_col,
                        y=y_col,
                        color="Typ",
                        hover_data=[group_col] if group_col != "Keine" else None,
                        title="Ausreißer pro Zeitraum (IQR 1.5)",
                        color_discrete_map={
                            "positiver Ausreißer": "#d32f2f",
                            "negativer Ausreißer": "#1976d2"
                        }
                    )
                else:
                    fig = go.Figure()
                    fig.update_layout(title="Keine Ausreißer gefunden (IQR-Methode)")
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                if st.button("Diese Ansicht speichern", key=f"save_{idx}"):
                    view = {
                        "name": analysis["name"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "x_col": x_col,
                        "y_col": y_col,
                        "group_col": group_col if group_col != "Keine" else None,
                        "fig": fig,
                        "type": analysis["type"]
                    }
                    st.session_state.saved_views.append(view)
                    st.success("Ansicht gespeichert!")
                    st.rerun()
    
    # ── Gespeicherte Ansichten ───────────────────────────────────
    st.markdown("### Gespeicherte Visualisierungen")
    
    if st.session_state.saved_views:
        st.write(f"{len(st.session_state.saved_views)} gespeicherte Ansichten")
        
        for i, view in enumerate(st.session_state.saved_views):
            colA, colB = st.columns([4,1])
            with colA:
                st.markdown(f"**{view['name']}**  ·  {view['timestamp']}")
                st.caption(f"X: {view['x_col']}  ·  Y: {view['y_col']}  ·  Gruppe: {view['group_col'] or '—'}")
            with colB:
                if st.button("Anzeigen", key=f"show_{i}"):
                    st.session_state.selected_view = i
                    st.rerun()
            
            st.markdown("---")
        
        # Detailansicht der ausgewählten Visualisierung
        if st.session_state.selected_view is not None:
            idx = st.session_state.selected_view
            view = st.session_state.saved_views[idx]
            
            st.markdown("## Ausgewählte gespeicherte Ansicht")
            st.markdown(f"**{view['name']}**   ·   gespeichert am {view['timestamp']}")
            st.caption(f"Spalten: X = {view['x_col']}, Y = {view['y_col']}, Gruppe = {view['group_col'] or 'keine'}")
            
            st.plotly_chart(view["fig"], use_container_width=True)
            
            if st.button("Detailansicht schließen"):
                st.session_state.selected_view = None
                st.rerun()
    
    else:
        st.info("Noch keine Ansichten gespeichert. Klicke bei einer der Analysen auf »Diese Ansicht speichern«.")

else:
    st.info("Bitte zuerst eine CSV-Datei hochladen.")

st.caption("Dashboard – nur interne Speicherung der Ansichten  •  2026")
