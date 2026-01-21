# dashboard.py
# Installation (einmalig im Terminal / Konsole):
# pip install streamlit pandas plotly

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(page_title="CSV Quick Dashboard", layout="wide")

st.title("CSV Dashboard – Datei hochladen & visualisieren")
st.markdown("Lade eine CSV-Datei hoch und erstelle danach interaktive Grafiken.")

# ── Datei-Upload ───────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "CSV-Datei auswählen",
    type=["csv"],
    help="Datei sollte Komma-separiert sein (,) und idealerweise eine Kopfzeile haben"
)

# Session State für die Daten
if "df" not in st.session_state:
    st.session_state.df = None
if "df_original" not in st.session_state:
    st.session_state.df_original = None

# ── Datei verarbeiten ──────────────────────────────────────────
if uploaded_file is not None:
    try:
        # Versuche verschiedene Encodings
        content = uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        try:
            content = uploaded_file.getvalue().decode("latin-1")
        except:
            content = uploaded_file.getvalue().decode("iso-8859-1", errors="replace")

    df = pd.read_csv(StringIO(content), sep=None, engine="python", on_bad_lines="warn")

    # Entferne komplett leere Zeilen/Spalten
    df = df.dropna(how="all").dropna(axis=1, how="all")

    st.session_state.df = df.copy()
    st.session_state.df_original = df.copy()

    st.success(f"Datei erfolgreich geladen – {len(df):,} Zeilen, {len(df.columns)} Spalten")

# ── Wenn Daten vorhanden sind ─────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df

    # ── Kurze Daten-Vorschau ────────────────────────────────
    with st.expander("Daten-Vorschau (erste 7 Zeilen)", expanded=False):
        st.dataframe(df.head(7))

    # ── Spalten-Info ────────────────────────────────────────
    with st.expander("Spalten & Datentypen", expanded=False):
        types = pd.DataFrame({
            "Spalte": df.columns,
            "Datentyp": df.dtypes.astype(str),
            "Fehlende Werte": df.isna().sum(),
            "eindeutige Werte": df.nunique()
        })
        st.dataframe(types)

    # ── Auswahlbereich ──────────────────────────────────────
    col1, col2, col3 = st.columns([2, 2, 1.4])

    with col1:
        chart_type = st.selectbox(
            "Diagramm-Typ",
            [
                "Liniendiagramm",
                "Balkendiagramm",
                "Gestapeltes Balkendiagramm",
                "Histogramm",
                "Boxplot",
                "Scatter / Punktdiagramm",
                "Kreisdiagramm (Pie)",
                "Treemap"
            ]
        )

    with col2:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
        datetime_cols = df.select_dtypes(include=["datetime", "datetime64"]).columns.tolist()

        all_cols = df.columns.tolist()

        if chart_type in ["Histogramm", "Boxplot"]:
            x = st.selectbox("Werte-Spalte (X)", numeric_cols if numeric_cols else all_cols, index=0 if numeric_cols else None)
            color = st.selectbox("Färben nach (optional)", ["Keine"] + cat_cols, index=0)
        elif chart_type == "Kreisdiagramm (Pie)" or chart_type == "Treemap":
            values = st.selectbox("Werte (Größe)", numeric_cols, index=0 if numeric_cols else None)
            names = st.selectbox("Kategorien/Namen", cat_cols + datetime_cols + ["Keine"], index=0)
        else:
            x = st.selectbox("X-Achse", all_cols, index=0)
            y = st.selectbox("Y-Achse", numeric_cols if numeric_cols else all_cols, index=1 if len(numeric_cols) > 1 else 0)
            color = st.selectbox("Färben / Gruppieren nach", ["Keine"] + cat_cols + datetime_cols, index=0)

    with col3:
        height = st.slider("Höhe des Diagramms (px)", 300, 900, 500, step=50)

    # ── Diagramm erstellen ──────────────────────────────────────
    try:
        if chart_type == "Liniendiagramm":
            fig = px.line(df, x=x, y=y, color=None if color == "Keine" else color,
                          title=f"{y} über {x}", height=height)

        elif chart_type == "Balkendiagramm":
            fig = px.bar(df, x=x, y=y, color=None if color == "Keine" else color,
                         title=f"{y} nach {x}", height=height)

        elif chart_type == "Gestapeltes Balkendiagramm":
            fig = px.bar(df, x=x, y=y, color=None if color == "Keine" else color,
                         barmode="stack", title=f"{y} gestapelt nach {x}", height=height)

        elif chart_type == "Histogramm":
            fig = px.histogram(df, x=x, color=None if color == "Keine" else color,
                               title=f"Verteilung von {x}", height=height)

        elif chart_type == "Boxplot":
            fig = px.box(df, x=x if color == "Keine" else color, y=x if color != "Keine" else y,
                         color=None if color == "Keine" else color,
                         title=f"Boxplot {x}", height=height)

        elif chart_type == "Scatter / Punktdiagramm":
            fig = px.scatter(df, x=x, y=y, color=None if color == "Keine" else color,
                             title=f"{y} vs {x}", height=height)

        elif chart_type == "Kreisdiagramm (Pie)":
            if names == "Keine":
                fig = px.pie(df, values=values, title=f"Verteilung von {values}", height=height)
            else:
                fig = px.pie(df, values=values, names=names, title=f"{values} nach {names}", height=height)

        elif chart_type == "Treemap":
            if names == "Keine":
                st.warning("Treemap benötigt Kategorien (Namen)")
                fig = None
            else:
                fig = px.treemap(df, path=[names], values=values,
                                 title=f"Treemap: {values} nach {names}", height=height)

        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Diagramm konnte nicht erstellt werden:\n{str(e)}")
        st.info("Mögliche Ursachen: falscher Datentyp, zu viele/fehlende Werte, ...")

    # ── Rohdaten-Tabelle am Ende (optional) ─────────────────────
    if st.checkbox("Komplette Tabelle anzeigen", value=False):
        st.dataframe(df)

else:
    st.info("↑ Lade bitte zuerst eine CSV-Datei hoch ↑")

st.markdown("---")
st.caption("Einfaches CSV-Dashboard • Streamlit + Plotly • 2025/26")