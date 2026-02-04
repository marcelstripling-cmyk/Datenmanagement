{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww34360\viewh21680\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # =============================================================================\
# Streamlit-Dashboard: Entwicklung der Gaspreise f\'fcr Haushaltskunden in Europa\
# =============================================================================\
#\
# Zweck:\
#   Interaktive Darstellung der halbj\'e4hrlichen Gaspreise f\'fcr Haushalte in Europa\
#   (inkl. aller Steuern und Abgaben) im Zeitraum 2020 bis 2025.\
#\
# Datenquelle:\
#   Eurostat \'96 Dataset nrg_pc_202 (Gaspreise f\'fcr Haushaltskunden, halbj\'e4hrlich)\
#   Band: DA / DC (mittlerer Verbrauch), Einheit: \'80/kWh\
#\
# Zeitraum:\
#   2020-H2 bis 2025-H1 (Stand: Ver\'f6ffentlichung Oktober/November 2025)\
#\
# Inhalt der Visualisierungen:\
#   - Zeitliche Preisentwicklung einzelner L\'e4nder mit Extremwerten\
#   - Vergleich von arithmetischem Mittel und Median je Land\
#   - Erkennung und Hervorhebung von Ausrei\'dfern mit variabler Schwelle\
#   - Boxplot-Darstellung der Preisverteilung aller L\'e4nder\
#\
# Verwendete Bibliotheken:\
#   streamlit, pandas, plotly.express, plotly.graph_objects\
\
import streamlit as st\
import pandas as pd\
import plotly.express as px\
import plotly.graph_objects as go\
from io import StringIO\
\
\
# \uc0\u9472 \u9472  Grundeinstellungen des Dashboards \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
st.set_page_config(\
    page_title="Gaspreise f\'fcr Haushaltskunden ab 2020-25",\
    layout="wide"\
)\
\
st.title("Gaspreise f\'fcr Haushaltskunden ab 2020-25")\
\
st.markdown(\
    "Daten: Haushalts-Gaspreise inkl. aller Steuern und Abgaben in \'80/kWh \'96 Halbjahreswerte"\
)\
\
\
# \uc0\u9472 \u9472  Eingebettete Rohdaten (CSV-Format) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
CSV_DATA = """\uc0\u65279 Unit;Tax;Currency;Geo;Time period;\'80/kWh;EU?\
... (vollst\'e4ndiger Datensatz \'96 siehe Originalcode)\
"""\
\
\
# \uc0\u9472 \u9472  Datenimport und -aufbereitung \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
@st.cache_data\
def load_data():\
    """\
    L\'e4dt die eingebetteten CSV-Daten und f\'fchrt grundlegende Bereinigungen durch.\
    \
    Returns\
    -------\
    pd.DataFrame\
        DataFrame mit den Spalten: Geo, Time period, \'80/kWh u.a.\
    """\
    df = pd.read_csv(StringIO(CSV_DATA), sep=";", decimal=".")\
    df = df.dropna(subset=["\'80/kWh"])\
    \
    # Umformatierung des Zeitraums: 2023-S2 \uc0\u8594  2023 H2\
    df["Time period"] = df["Time period"].str.replace("-S", " H")\
    \
    return df\
\
\
df = load_data()\
countries = sorted(df["Geo"].unique())\
\
\
# \uc0\u9472 \u9472  Registerkarten (Tabs) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
tab1, tab2, tab3, tab4 = st.tabs([\
    "1. Preisspanne teuer \uc0\u8596  g\'fcnstig",\
    "2. Durchschnitt vs. Median pro Land",\
    "3. Ausrei\'dfer \uc0\u8805  \'b1 XX % vom Mittelwert",\
    "4. Boxplot \'96 Preisverteilung aller L\'e4nder"\
])\
\
\
# \uc0\u9472 \u9472  Tab 1: Zeitliche Preisentwicklung eines Landes \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
with tab1:\
    st.subheader("1. Preisentwicklung und Spanne eines Landes")\
    \
    selected_country = st.selectbox(\
        "Land ausw\'e4hlen",\
        countries,\
        index=countries.index("Germany") if "Germany" in countries else 0,\
        key="tab1"\
    )\
    \
    df_country = df[df["Geo"] == selected_country]\
    \
    fig = go.Figure()\
    fig.add_trace(go.Scatter(\
        x    = df_country["Time period"],\
        y    = df_country["\'80/kWh"],\
        mode = 'lines+markers',\
        name = 'Preisverlauf',\
        line = dict(color='royalblue', width=3)\
    ))\
    \
    fig.add_hline(y=df_country["\'80/kWh"].max(), line_dash="dash", line_color="red",\
                  annotation_text=f"Max: \{df_country['\'80/kWh'].max():.4f\}")\
    fig.add_hline(y=df_country["\'80/kWh"].min(), line_dash="dash", line_color="green",\
                  annotation_text=f"Min: \{df_country['\'80/kWh'].min():.4f\}")\
    \
    fig.update_layout(\
        title  = f"Preisentwicklung \{selected_country\}",\
        xaxis_title = "Zeitraum",\
        yaxis_title = "\'80/kWh",\
        height = 520,\
        template = "plotly_white"\
    )\
    \
    st.plotly_chart(fig, use_container_width=True)\
\
\
# \uc0\u9472 \u9472  Tab 2: Vergleich Mittelwert und Median \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
with tab2:\
    st.subheader("2. Arithmetisches Mittel und Median im Vergleich")\
    \
    summary = df.groupby("Geo")["\'80/kWh"].agg(\
        Durchschnitt = 'mean',\
        Median      = 'median'\
    ).reset_index()\
    \
    melted = summary.melt(\
        id_vars       = "Geo",\
        value_vars    = ["Durchschnitt", "Median"],\
        var_name      = "Ma\'df",\
        value_name    = "\'80/kWh"\
    )\
    \
    fig = px.bar(\
        melted,\
        x        = "Geo",\
        y        = "\'80/kWh",\
        color    = "Ma\'df",\
        barmode  = "group",\
        text_auto = ".4f",\
        title    = "Durchschnitt und Median pro Land",\
        height   = 580\
    )\
    \
    fig.update_layout(\
        xaxis_title = "Land",\
        yaxis_title = "\'80/kWh",\
        template    = "plotly_white"\
    )\
    \
    st.plotly_chart(fig, use_container_width=True)\
\
\
# \uc0\u9472 \u9472  Tab 3: Ausrei\'dfererkennung mit anpassbarer Schwelle \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
with tab3:\
    st.subheader("3. Ausrei\'dfererkennung mit variabler Schwelle")\
    \
    st.markdown("""\
    **Definition Ausrei\'dfer**  \
    Werte mit einer Abweichung von \uc0\u8805  20\'9630 % vom arithmetischen Mittelwert des jeweiligen Landes  \
    gelten als potenzielle Ausrei\'dfer. Ab etwa 50 % Abweichung ist dies in der Regel sehr wahrscheinlich.\
    """)\
    \
    selected_country = st.selectbox(\
        "Land ausw\'e4hlen",\
        countries,\
        index=countries.index("Germany") if "Germany" in countries else 0,\
        key="tab3"\
    )\
    \
    threshold_pct = st.slider(\
        "Mindestabweichung vom Mittelwert (%)",\
        min_value = 5.0,\
        max_value = 100.0,\
        value     = 20.0,\
        step      = 2.5,\
        format    = "%.1f %%"\
    )\
    \
    df_sel = df[df["Geo"] == selected_country].copy()\
    mean_val = df_sel["\'80/kWh"].mean()\
    \
    df_sel["Abweichung_%"]   = ((df_sel["\'80/kWh"] - mean_val) / mean_val * 100).round(1)\
    df_sel["Abs_Abweichung"] = df_sel["Abweichung_%"].abs()\
    \
    df_sel["Kategorie"] = f"innerhalb \'b1\{threshold_pct\}%"\
    df_sel.loc[df_sel["Abweichung_%"] >= threshold_pct,  "Kategorie"] = f"\uc0\u8805  +\{threshold_pct\}%"\
    df_sel.loc[df_sel["Abweichung_%"] <= -threshold_pct, "Kategorie"] = f"\uc0\u8804  -\{threshold_pct\}%"\
    \
    color_map = \{\
        f"innerhalb \'b1\{threshold_pct\}%":  "#95a5a6",\
        f"\uc0\u8805  +\{threshold_pct\}%":          "#e74c3c",\
        f"\uc0\u8804  -\{threshold_pct\}%":          "#3498db"\
    \}\
    \
    fig = px.scatter(\
        df_sel,\
        x                = "Time period",\
        y                = "\'80/kWh",\
        color            = "Kategorie",\
        size             = "Abs_Abweichung",\
        size_max         = 20,\
        title            = f"\{selected_country\} \'96 Ausrei\'dfer ab \'b1\{threshold_pct\}% vom Mittelwert",\
        height           = 540,\
        color_discrete_map = color_map\
    )\
    \
    fig.add_hline(y=mean_val, line_dash="dot", line_color="black",\
                  annotation_text=f"Mittelwert: \{mean_val:.4f\}")\
    fig.add_hline(y=mean_val*(1 + threshold_pct/100), line_dash="dash", line_color="red")\
    fig.add_hline(y=mean_val*(1 - threshold_pct/100), line_dash="dash", line_color="blue")\
    \
    fig.update_layout(template="plotly_white", legend_title="Abweichung")\
    st.plotly_chart(fig, use_container_width=True)\
\
\
# \uc0\u9472 \u9472  Tab 4: Boxplot-Darstellung aller L\'e4nder \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
with tab4:\
    st.subheader("4. Preisverteilung aller L\'e4nder (Boxplot)")\
    \
    fig = px.box(\
        df,\
        x       = "Geo",\
        y       = "\'80/kWh",\
        points  = "outliers",\
        title   = "Verteilung der Gaspreise pro Land (2020\'962025)",\
        height  = 620,\
        color   = "Geo"\
    )\
    \
    fig.update_layout(\
        xaxis_title = "Land",\
        yaxis_title = "\'80/kWh",\
        showlegend  = False,\
        template    = "plotly_white"\
    )\
    \
    st.plotly_chart(fig, use_container_width=True)\
    \
    st.info(\
        "Boxplot-Elemente:\\n"\
        "\'95 Mittellinie = Median\\n"\
        "\'95 Box = 25.\'9675. Perzentil (IQR)\\n"\
        "\'95 Whisker = 1,5 \'d7 IQR\\n"\
        "\'95 Einzelne Punkte = statistische Ausrei\'dfer"\
    )\
\
\
# \uc0\u9472 \u9472  Fu\'dfzeile \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
\
st.caption(\
    "Dashboard \'95 Gaspreise f\'fcr Haushaltskunden in Europa \'95 Datenstand 2025-H1 \'95 Februar 2026"\
)}