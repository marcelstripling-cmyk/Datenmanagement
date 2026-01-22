# dashboard.py
# pip install streamlit pandas plotly

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import StringIO

st.set_page_config(page_title="Gaspreise EU Dashboard", layout="wide")

st.title("Gaspreise EU – Halbjahresvergleich (2020–2025)")
st.markdown("Daten: Haushalts-Gaspreise (inkl. Steuern & Abgaben) in € pro kWh – Halbjahreswerte")

# ── Daten direkt im Code (aus deiner Datei) ────────────────────────────────
CSV_DATA = """﻿Unit;Tax;Currency;Geo;Zeit;Preis
Kilowatt-hour;All taxes and levies included;Euro;Austria;2020-S2;0.0656
Kilowatt-hour;All taxes and levies included;Euro;Austria;2021-S1;0.0636
Kilowatt-hour;All taxes and levies included;Euro;Austria;2021-S2;0.0695
Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S1;0.0767
Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S2;0.1235
Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S1;0.1560
Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S2;0.1477
Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S1;0.1379
Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S2;0.1237
Kilowatt-hour;All taxes and levies included;Euro;Austria;2025-S1;0.1220
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2020-S2;0.0498
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2021-S1;0.0468
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2021-S2;0.0676
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S1;0.0943
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S2;0.1363
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S1;0.1146
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S2;0.0994
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S1;0.0801
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S2;0.0903
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2025-S1;0.0919
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2020-S2;0.0348
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2021-S1;0.0368
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2021-S2;0.0708
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S1;0.0764
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S2;0.1173
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S1;0.0879
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S2;0.0703
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S1;0.0619
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S2;0.0649
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2025-S1;0.0765
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2020-S2;0.0558
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2021-S1;0.0562
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2021-S2;0.0554
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S1;0.0696
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S2;0.1066
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S1;0.1138
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S2;0.1125
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S1;0.1085
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S2;0.1029
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2025-S1;0.0967
Kilowatt-hour;All taxes and levies included;Euro;Germany;2020-S2;0.0620
Kilowatt-hour;All taxes and levies included;Euro;Germany;2021-S1;0.0647
Kilowatt-hour;All taxes and levies included;Euro;Germany;2021-S2;0.0692
Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S1;0.0806
Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S2;0.0941
Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S1;0.1230
Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S2;0.1145
Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S1;0.1198
Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S2;0.1238
Kilowatt-hour;All taxes and levies included;Euro;Germany;2025-S1;0.1216
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2020-S2;0.0747
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2021-S1;0.0895
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2021-S2;0.1247
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S1;0.1509
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S2;0.2084
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S1;0.1655
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S2;0.1220
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S1;0.1223
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S2;0.1313
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2025-S1;0.1306
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2020-S2;0.0411
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2021-S1;0.0435
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2021-S2;0.0750
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S1;0.1106
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S2;0.1089
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S1;0.1099
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S2;0.0791
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S1;0.0691
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S2;0.0788
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2025-S1;0.0856
Kilowatt-hour;All taxes and levies included;Euro;Greece;2020-S2;0.0517
Kilowatt-hour;All taxes and levies included;Euro;Greece;2021-S1;0.0449
Kilowatt-hour;All taxes and levies included;Euro;Greece;2021-S2;0.1014
Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S1;0.0821
Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S2;0.1599
Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S1;0.1187
Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S2;0.0926
Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S1;0.0744
Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S2;0.0945
Kilowatt-hour;All taxes and levies included;Euro;Greece;2025-S1;0.0863
Kilowatt-hour;All taxes and levies included;Euro;Spain;2020-S2;0.0890
Kilowatt-hour;All taxes and levies included;Euro;Spain;2021-S1;0.0691
Kilowatt-hour;All taxes and levies included;Euro;Spain;2021-S2;0.1082
Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S1;0.0897
Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S2;0.1574
Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S1;0.1077
Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S2;0.1010
Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S1;0.0858
Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S2;0.0901
Kilowatt-hour;All taxes and levies included;Euro;Spain;2025-S1;0.0859
Kilowatt-hour;All taxes and levies included;Euro;France;2020-S2;0.0751
Kilowatt-hour;All taxes and levies included;Euro;France;2021-S1;0.0691
Kilowatt-hour;All taxes and levies included;Euro;France;2021-S2;0.0788
Kilowatt-hour;All taxes and levies included;Euro;France;2022-S1;0.0859
Kilowatt-hour;All taxes and levies included;Euro;France;2022-S2;0.1008
Kilowatt-hour;All taxes and levies included;Euro;France;2023-S1;0.1044
Kilowatt-hour;All taxes and levies included;Euro;France;2023-S2;0.1181
Kilowatt-hour;All taxes and levies included;Euro;France;2024-S1;0.1197
Kilowatt-hour;All taxes and levies included;Euro;France;2024-S2;0.1331
Kilowatt-hour;All taxes and levies included;Euro;France;2025-S1;0.1298
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2020-S2;0.0377
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2021-S1;0.0374
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2021-S2;0.0398
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S1;0.0412
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S2;0.0450
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S1;0.0443
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S2;0.0457
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S1;0.0447
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S2;0.0456
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2025-S1;0.0461
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2020-S2;0.0308
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S1;0.0307
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S2;0.0305
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S1;0.0291
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S2;0.0349
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S1;0.0337
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S2;0.0335
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S1;0.0275
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S2;0.0315
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2025-S1;0.0307
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2020-S2;0.0702
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S1;0.0620
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S2;0.0783
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S1;0.0847
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S2;0.1544
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S1;0.1465
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S2;0.1638
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S1;0.1271
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S2;0.1347
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2025-S1;0.1218
Kilowatt-hour;All taxes and levies included;Euro;Italy;2020-S2;0.0897
Kilowatt-hour;All taxes and levies included;Euro;Italy;2021-S1;0.0703
Kilowatt-hour;All taxes and levies included;Euro;Italy;2021-S2;0.1005
Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S1;0.0986
Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S2;0.1310
Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S1;0.0981
Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S2;0.1347
Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S1;0.1140
Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S2;0.1586
Kilowatt-hour;All taxes and levies included;Euro;Italy;2025-S1;0.1240
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2020-S2;0.0295
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2021-S1;0.0279
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2021-S2;0.0410
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S1;0.0587
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S2;0.1288
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S1;0.1849
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S2;0.1454
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S1;0.0739
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S2;0.0596
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2025-S1;0.0667
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2020-S2;0.0366
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2021-S1;0.0438
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2021-S2;0.0639
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S1;0.0856
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S2;0.0891
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S1;0.0875
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S2;0.0850
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2024-S1;0.0883
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2024-S2;0.0732
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2025-S1;0.0929
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2020-S2;0.0280
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2021-S1;0.0297
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2021-S2;0.0432
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S1;0.0462
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S2;0.1111
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S1;0.1105
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S2;0.0901
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S1;0.0923
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S2;0.0880
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2025-S1;0.0832
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2020-S2;0.1084
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S1;0.1005
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S2;0.1167
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S1;0.1287
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S2;0.1923
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S1;0.1953
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S2;0.1548
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S1;0.1647
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S2;0.1698
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2025-S1;0.1617
Kilowatt-hour;All taxes and levies included;Euro;Poland;2020-S2;0.0419
Kilowatt-hour;All taxes and levies included;Euro;Poland;2021-S1;0.0376
Kilowatt-hour;All taxes and levies included;Euro;Poland;2021-S2;0.0473
Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S1;0.0549
Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S2;0.0553
Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S1;0.0683
Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S2;0.0730
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2020-S2;0.0783
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2021-S1;0.0762
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2021-S2;0.0773
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S1;0.0837
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S2;0.1277
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S1;0.1406
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S2;0.1374
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2024-S1;0.1192
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2024-S2;0.1366
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2025-S1;0.1265
Kilowatt-hour;All taxes and levies included;Euro;Romania;2020-S2;0.0320
Kilowatt-hour;All taxes and levies included;Euro;Romania;2021-S1;0.0317
Kilowatt-hour;All taxes and levies included;Euro;Romania;2021-S2;0.0475
Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S1;0.0611
Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S2;0.1265
Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S1;0.0548
Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S2;0.0558
Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S1;0.0581
Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S2;0.0541
Kilowatt-hour;All taxes and levies included;Euro;Romania;2025-S1;0.0559
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2020-S2;0.1422
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S1;0.1438
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S2;0.2058
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S1;0.2216
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S2;0.2751
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S1;0.2189
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S2;0.2070
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S1;0.1760
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S2;0.1893
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2025-S1;0.2128
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2020-S2;0.0549
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2021-S1;0.0547
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2021-S2;0.0587
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S1;0.0691
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S2;0.0942
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S1;0.0971
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S2;0.1107
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S1;0.0972
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S2;0.0909
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2025-S1;0.0849
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2020-S2;0.0480
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2021-S1;0.0411
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2021-S2;0.0423
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S1;0.0488
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S2;0.0499
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S1;0.0571
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S2;0.0611
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S1;0.0585
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S2;0.0600
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2025-S1;0.0587"""

@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(CSV_DATA), sep=";", decimal=".", thousands=None)
    df = df.dropna(how="all").dropna(axis=1, how="all")
    # Zeit-Spalte etwas lesbarer machen (optional)
    df["Zeit"] = df["Zeit"].str.replace("-S", " H")
    return df

df = load_data()

# ── Session State für gespeicherte Views ───────────────────────────────
if "saved_views" not in st.session_state:
    st.session_state.saved_views = []

if "selected_view" not in st.session_state:
    st.session_state.selected_view = None

# ── Verfügbare Visualisierungen (hier kannst du beliebig viele hinzufügen!) ──
available_charts = [
    {"id": "range_all",       "name": "1. Preisspanne (Min–Max) über alle Länder",   "desc": "Schwankung teuer ↔ günstig pro Halbjahr"},
    {"id": "median_mean",     "name": "2. Median vs. Durchschnitt pro Halbjahr",     "desc": "Vergleich Median und Mittelwert"},
    {"id": "outliers",        "name": "3. Positive & negative Ausreißer",            "desc": "IQR-Methode pro Halbjahr"},
    {"id": "line_countries",  "name": "Linien – Entwicklung pro Land",               "desc": "Jedes Land als eigene Linie"},
    {"id": "area_countries",  "name": "Flächen – gestapelt pro Land",                "desc": "Gestapelte Flächenentwicklung"},
    {"id": "box_halfyear",    "name": "Boxplot pro Halbjahr",                        "desc": "Verteilung aller Länder pro Zeitpunkt"},
    {"id": "bar_top10",       "name": "Top 10 teuerste Länder pro Halbjahr",         "desc": "Balken – Rangliste teuerste Preise"},
    {"id": "heatmap",         "name": "Heatmap – Preis nach Land & Halbjahr",        "desc": "Farbcodierte Matrix"},
    {"id": "violin",          "name": "Violin-Plot pro Land",                        "desc": "Dichte + Verteilung pro Land"},
]

# ── Auswahl der Visualisierung ────────────────────────────────────────────
st.subheader("Visualisierung auswählen")
chart_option = st.selectbox(
    "Welche Darstellung möchtest du sehen?",
    options=[c["name"] for c in available_charts],
    index=0
)

# Gefundene Option
selected_chart = next(c for c in available_charts if c["name"] == chart_option)

# ── Plot-Logik ────────────────────────────────────────────────────────────
fig = None
x = "Zeit"
y = "Preis"
color = "Geo"

if selected_chart["id"] == "range_all":
    grouped = df.groupby(x)[y].agg(['min','max']).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=grouped[x], y=grouped['max'], name="Max", line=dict(color='red')))
    fig.add_trace(go.Scatter(x=grouped[x], y=grouped['min'], name="Min", line=dict(color='green')))
    fig.add_trace(go.Scatter(x=grouped[x], y=grouped['max'], fill='tonexty', fillcolor='rgba(255,0,0,0.08)'))
    fig.update_layout(title="Preisspanne (Min–Max) über alle Länder", hovermode="x unified")

elif selected_chart["id"] == "median_mean":
    grouped = df.groupby(x)[y].agg(['mean','median']).reset_index()
    fig = px.line(
        grouped.melt(id_vars=x, value_vars=['mean','median']),
        x=x, y="value", color="variable",
        title="Median vs. Durchschnitt pro Halbjahr",
        labels={"value": "Preis €/kWh", "variable": "Maß"}
    )

elif selected_chart["id"] == "outliers":
    def flag_out(g):
        q1, q3 = g[y].quantile([0.25, 0.75])
        iqr = q3 - q1
        g['Ausreißer'] = 'normal'
        g.loc[g[y] < q1 - 1.5*iqr, 'Ausreißer'] = 'negativ'
        g.loc[g[y] > q3 + 1.5*iqr, 'Ausreißer'] = 'positiv'
        return g
    df_out = df.groupby(x).apply(flag_out).reset_index(drop=True)
    outliers = df_out[df_out['Ausreißer'] != 'normal']
    if not outliers.empty:
        fig = px.scatter(outliers, x=x, y=y, color='Ausreißer', hover_name=color,
                         title="Ausreißer (IQR 1.5×)", color_discrete_map={"positiv":"red", "negativ":"blue"})
    else:
        fig = go.Figure().update_layout(title="Keine Ausreißer gefunden")

elif selected_chart["id"] == "line_countries":
    fig = px.line(df, x=x, y=y, color=color, title="Preisentwicklung pro Land",
                  markers=True, hover_name=color)

elif selected_chart["id"] == "area_countries":
    fig = px.area(df, x=x, y=y, color=color, title="Gestapelte Preisentwicklung")

elif selected_chart["id"] == "box_halfyear":
    fig = px.box(df, x=x, y=y, color=x, title="Verteilung pro Halbjahr",
                 points="all", hover_name=color)

elif selected_chart["id"] == "bar_top10":
    latest = df[df[x] == df[x].max()]
    top10 = latest.nlargest(10, y)
    fig = px.bar(top10, x=color, y=y, title=f"Top 10 teuerste Länder ({latest[x].iloc[0]})",
                 text_auto=True)

elif selected_chart["id"] == "heatmap":
    pivot = df.pivot(index=color, columns=x, values=y)
    fig = px.imshow(pivot, title="Heatmap: Preis nach Land & Halbjahr",
                    color_continuous_scale="RdYlGn_r", text_auto=True)

elif selected_chart["id"] == "violin":
    fig = px.violin(df, x=color, y=y, color=color, box=True, points="all",
                    title="Verteilung & Dichte pro Land")

if fig:
    fig.update_layout(height=550, hovermode="closest")
    st.plotly_chart(fig, use_container_width=True)

    # Speichern-Button
    if st.button(f"→ Diese Ansicht speichern ({selected_chart['name']})", type="primary"):
        view = {
            "name": selected_chart["name"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "chart_id": selected_chart["id"],
            "fig": fig
        }
        st.session_state.saved_views.append(view)
        st.success("Gespeichert!")
        st.rerun()

# ── Gespeicherte Ansichten ────────────────────────────────────────────────
st.markdown("---")
st.subheader("Gespeicherte Visualisierungen")

if st.session_state.saved_views:
    for i, view in enumerate(st.session_state.saved_views):
        cols = st.columns([5,1])
        with cols[0]:
            st.write(f"**{view['name']}**  ·  {view['timestamp']}")
        with cols[1]:
            if st.button("Anzeigen", key=f"load_{i}"):
                st.session_state.selected_view = i
                st.rerun()

    if st.session_state.selected_view is not None:
        v = st.session_state.saved_views[st.session_state.selected_view]
        st.markdown(f"### {v['name']}  –  {v['timestamp']}")
        st.plotly_chart(v["fig"], use_container_width=True)

        if st.button("Schließen / zurück"):
            st.session_state.selected_view = None
            st.rerun()
else:
    st.info("Noch nichts gespeichert. Wähle eine Visualisierung und klicke oben auf »speichern«.")

st.caption("Datenquelle: deine GaspreiseDaten2.csv • Dashboard erweiterbar • 2026")
