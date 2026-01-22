import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(page_title="Gaspreise Analyse", layout="wide")

st.title("Gaspreise EU – Analyse Halbjahresdaten")
st.markdown("Daten: Haushalts-Gaspreise inkl. Steuern & Abgaben in €/kWh")

# ── Daten einbinden ────────────────────────────────────────────────────────
CSV_DATA = """﻿Unit;Tax;Currency;Geo;Time period;€/kWh;EU?
Kilowatt-hour;All taxes and levies included;Euro;Austria;2020-S2;0.0656;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2021-S1;0.0636;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2021-S2;0.0695;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S1;0.0767;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S2;0.1235;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S1;0.1560;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S2;0.1477;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S1;0.1379;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S2;0.1237;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2025-S1;0.1220;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2020-S2;0.0498;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2021-S1;0.0468;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2021-S2;0.0676;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S1;0.0943;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S2;0.1363;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S1;0.1146;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S2;0.0994;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S1;0.0801;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S2;0.0903;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2025-S1;0.0919;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2020-S2;0.0348;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2021-S1;0.0368;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2021-S2;0.0708;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S1;0.0764;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S2;0.1173;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S1;0.0879;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S2;0.0703;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S1;0.0619;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S2;0.0649;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2025-S1;0.0765;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2020-S2;0.0558;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2021-S1;0.0562;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2021-S2;0.0554;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S1;0.0696;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S2;0.1066;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S1;0.1138;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S2;0.1125;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S1;0.1085;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S2;0.1029;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2025-S1;0.0967;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2020-S2;0.0620;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2021-S1;0.0647;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2021-S2;0.0692;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S1;0.0806;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S2;0.0941;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S1;0.1230;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S2;0.1145;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S1;0.1198;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S2;0.1238;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2025-S1;0.1216;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2020-S2;0.0747;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2021-S1;0.0895;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2021-S2;0.1247;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S1;0.1509;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S2;0.2084;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S1;0.1655;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S2;0.1220;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S1;0.1223;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S2;0.1313;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2025-S1;0.1306;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2020-S2;0.0411;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2021-S1;0.0435;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2021-S2;0.0750;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S1;0.1106;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S2;0.1089;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S1;0.1099;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S2;0.0791;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S2;0.0788;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2025-S1;0.0856;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2020-S2;0.0517;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2021-S1;0.0449;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2021-S2;0.1014;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S1;0.0821;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S2;0.1599;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S1;0.1187;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S2;0.0926;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S1;0.0744;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S2;0.0945;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2025-S1;0.0863;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2020-S2;0.0890;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2021-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2021-S2;0.1082;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S1;0.0897;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S2;0.1574;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S1;0.1077;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S2;0.1010;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S1;0.0858;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S2;0.0901;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2025-S1;0.0859;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2020-S2;0.0751;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2021-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2021-S2;0.0788;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2022-S1;0.0859;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2022-S2;0.1008;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2023-S1;0.1044;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2023-S2;0.1181;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2024-S1;0.1197;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2024-S2;0.1331;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2025-S1;0.1298;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2020-S2;0.0377;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2021-S1;0.0374;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2021-S2;0.0398;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S1;0.0412;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S2;0.0450;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S1;0.0443;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S2;0.0457;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S1;0.0447;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S2;0.0456;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2025-S1;0.0461;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2020-S2;0.0308;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S1;0.0307;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S2;0.0305;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S1;0.0291;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S2;0.0349;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S1;0.0337;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S2;0.0335;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S1;0.0275;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S2;0.0315;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2025-S1;0.0307;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2020-S2;0.0702;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S1;0.0620;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S2;0.0783;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S1;0.0847;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S2;0.1544;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S1;0.1465;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S2;0.1638;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S1;0.1271;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S2;0.1347;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2025-S1;0.1218;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2020-S2;0.0897;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2021-S1;0.0703;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2021-S2;0.1005;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S1;0.0986;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S2;0.1310;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S1;0.0981;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S2;0.1347;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S1;0.1140;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S2;0.1586;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2025-S1;0.1240;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2020-S2;0.0295;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2021-S1;0.0279;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2021-S2;0.0410;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S1;0.0587;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S2;0.1288;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S1;0.1849;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S2;0.1454;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S1;0.0739;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S2;0.0596;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2025-S1;0.0667;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2020-S2;0.0366;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2021-S1;0.0438;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2021-S2;0.0639;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S1;0.0856;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S2;0.0891;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S1;0.0875;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S2;0.0850;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2024-S1;0.0883;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2024-S2;0.0732;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2025-S1;0.0929;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2020-S2;0.0280;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2021-S1;0.0297;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2021-S2;0.0432;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S1;0.0462;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S2;0.1111;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S1;0.1105;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S2;0.0901;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S1;0.0923;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S2;0.0880;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2025-S1;0.0832;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2020-S2;0.1084;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S1;0.1005;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S2;0.1167;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S1;0.1287;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S2;0.1923;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S1;0.1953;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S2;0.1548;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S1;0.1647;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S2;0.1698;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2025-S1;0.1617;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2020-S2;0.0419;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2021-S1;0.0376;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2021-S2;0.0473;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S1;0.0549;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S2;0.0553;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S1;0.0683;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S2;0.0730;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2020-S2;0.0783;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2021-S1;0.0762;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2021-S2;0.0773;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S1;0.0837;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S2;0.1277;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S1;0.1406;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S2;0.1374;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2024-S1;0.1192;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2024-S2;0.1366;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2025-S1;0.1265;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2020-S2;0.0320;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2021-S1;0.0317;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2021-S2;0.0475;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S1;0.0611;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S2;0.1265;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S1;0.0548;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S2;0.0558;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S1;0.0581;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S2;0.0541;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2025-S1;0.0559;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2020-S2;0.1422;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S1;0.1438;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S2;0.2058;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S1;0.2216;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S2;0.2751;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S1;0.2189;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S2;0.2070;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S1;0.1760;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S2;0.1893;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2025-S1;0.2128;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2020-S2;0.0549;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2021-S1;0.0547;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2021-S2;0.0587;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S2;0.0942;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S1;0.0971;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S2;0.1107;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S1;0.0972;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S2;0.0909;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2025-S1;0.0849;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2020-S2;0.0480;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2021-S1;0.0411;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2021-S2;0.0423;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S1;0.0488;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S2;0.0499;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S1;0.0571;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S2;0.0611;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S1;0.0585;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S2;0.0600;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2025-S1;0.0587;WAHR"""

@st.cache_data
def load_data():
    df = pd.read_csv(StringIO(CSV_DATA), sep=";", decimal=".")
    df = df.dropna(subset=["€/kWh"])
    df["Time period"] = df["Time period"].str.replace("-S", " H")
    return df

df = load_data()

countries = sorted(df["Geo"].unique())

tab1, tab2, tab3 = st.tabs([
    "1. Preisspanne teuer ↔ günstig",
    "2. Durchschnitt vs. Median pro Land",
    "3. Ausreißer ≥ ± XX % vom Mittelwert"
])

# ────────────────────────────────────────────────────────────────────────────
# Tab 1 – Preisverlauf mit Min/Max-Linien
# ────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("1. Wie schwankt der Preis zwischen teuer und günstig?")
    
    selected_country_1 = st.selectbox(
        "Land auswählen",
        options=countries,
        index=countries.index("Germany") if "Germany" in countries else 0,
        key="country_tab1"
    )
    
    df_country = df[df["Geo"] == selected_country_1]
    
    if not df_country.empty:
        fig1 = go.Figure()
        
        fig1.add_trace(go.Scatter(
            x=df_country["Time period"],
            y=df_country["€/kWh"],
            mode='lines+markers',
            name='Preis €/kWh',
            line=dict(color='royalblue', width=2.5),
            marker=dict(size=8)
        ))
        
        fig1.add_hline(y=df_country["€/kWh"].max(), line_dash="dash", line_color="red",
                       annotation_text=f"Max: {df_country['€/kWh'].max():.4f}", 
                       annotation_position="top right")
        
        fig1.add_hline(y=df_country["€/kWh"].min(), line_dash="dash", line_color="green",
                       annotation_text=f"Min: {df_country['€/kWh'].min():.4f}", 
                       annotation_position="bottom right")
        
        fig1.update_layout(
            title=f"Preisentwicklung {selected_country_1}",
            xaxis_title="Time period",
            yaxis_title="€/kWh",
            height=520,
            hovermode="x unified",
            template="plotly_white"
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Keine Daten für dieses Land.")

# ────────────────────────────────────────────────────────────────────────────
# Tab 2 – Balkendiagramm Durchschnitt & Median (ohne gestrichelte Abweichungslinie)
# ────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("2. Unterschied Durchschnitt & Median im Preis")
    
    summary = df.groupby("Geo")["€/kWh"].agg(
        Durchschnitt='mean',
        Median='median'
    ).reset_index()
    
    summary["Abweichung (%)"] = (
        (summary["Durchschnitt"] - summary["Median"]) / summary["Median"] * 100
    ).round(1)
    
    summary_melt = summary.melt(
        id_vars=["Geo", "Abweichung (%)"],
        value_vars=["Durchschnitt", "Median"],
        var_name="Maß",
        value_name="€/kWh"
    )
    
    fig2 = px.bar(
        summary_melt,
        x="Geo",
        y="€/kWh",
        color="Maß",
        barmode="group",
        text_auto=".4f",
        title="Durchschnitt und Median pro Land",
        height=580
    )
    
    # → Die gestrichelte Linie wurde entfernt
    
    fig2.update_layout(
        xaxis_title="Land (Geo)",
        yaxis_title="€/kWh",
        legend_title="Maß",
        hovermode="x unified",
        template="plotly_white"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Optional: Die %-Abweichung trotzdem noch als Text in der Tabelle zeigen
    st.write("**Abweichung Durchschnitt vs. Median in Prozent**")
    st.dataframe(
        summary[["Geo", "Durchschnitt", "Median", "Abweichung (%)"]]
        .style.format({
            "Durchschnitt": "{:.4f}",
            "Median": "{:.4f}",
            "Abweichung (%)": "{:+.1f} %"
        }),
        use_container_width=True,
        hide_index=True
    )

# ────────────────────────────────────────────────────────────────────────────
# Tab 3 – Punktwolkendiagramm mit Slider
# ────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("3. Ausreißer – Punktwolke mit anpassbarer Schwelle")
    
    selected_country_3 = st.selectbox(
        "Land auswählen",
        options=countries,
        index=countries.index("Germany") if "Germany" in countries else 0,
        key="country_tab3"
    )
    
    threshold_pct = st.slider(
        "Mindest-Abweichung vom Mittelwert für Ausreißer",
        min_value=5.0,
        max_value=50.0,
        value=20.0,
        step=2.5,
        format="%.1f %%"
    )
    
    df_country3 = df[df["Geo"] == selected_country_3].copy()
    
    if not df_country3.empty:
        mean_value = df_country3["€/kWh"].mean()
        
        df_country3["Abweichung_%"] = ((df_country3["€/kWh"] - mean_value) / mean_value * 100).round(1)
        df_country3["Abs_Abweichung"] = df_country3["Abweichung_%"].abs()
        
        df_country3["Ausreißer"] = f"innerhalb ±{threshold_pct}%"
        df_country3.loc[df_country3["Abweichung_%"] >= threshold_pct, "Ausreißer"] = f"≥ +{threshold_pct}%"
        df_country3.loc[df_country3["Abweichung_%"] <= -threshold_pct, "Ausreißer"] = f"≤ -{threshold_pct}%"
        
        color_map = {
            f"innerhalb ±{threshold_pct}%": "#95a5a6",
            f"≥ +{threshold_pct}%": "#e74c3c",
            f"≤ -{threshold_pct}%": "#3498db"
        }
        
        fig3 = px.scatter(
            df_country3,
            x="Time period",
            y="€/kWh",
            color="Ausreißer",
            size="Abs_Abweichung",
            size_max=20,
            hover_data=["Abweichung_%", "Time period", "€/kWh"],
            title=f"{selected_country_3} – Ausreißer ≥ ±{threshold_pct}% vom Mittelwert",
            height=540,
            color_discrete_map=color_map
        )
        
        fig3.add_hline(
            y=mean_value,
            line_dash="dot",
            line_color="black",
            annotation_text=f"Mittelwert: {mean_value:.4f} €/kWh",
            annotation_position="top right"
        )
        
        fig3.add_hline(
            y=mean_value * (1 + threshold_pct/100),
            line_dash="dash",
            line_color="red",
            line_width=1.2,
            annotation_text=f"+{threshold_pct}%",
            annotation_position="top right"
        )
        
        fig3.add_hline(
            y=mean_value * (1 - threshold_pct/100),
            line_dash="dash",
            line_color="blue",
            line_width=1.2,
            annotation_text=f"–{threshold_pct}%",
            annotation_position="bottom right"
        )
        
        fig3.update_traces(
            marker=dict(opacity=0.9, line=dict(width=1, color='DarkSlateGrey'))
        )
        
        fig3.update_layout(
            xaxis_title="Time period",
            yaxis_title="€/kWh",
            hovermode="closest",
            template="plotly_white",
            legend_title="Ausreißer-Typ"
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        outliers = df_country3[df_country3["Ausreißer"] != f"innerhalb ±{threshold_pct}%"]
        if not outliers.empty:
            st.info(f"Bei ±{threshold_pct}% Schwelle → {len(outliers)} Ausreißer gefunden")
            st.dataframe(
                outliers[["Time period", "€/kWh", "Abweichung_%", "Ausreißer"]]
                .sort_values("Abweichung_%", ascending=False)
                .style.format({"€/kWh": "{:.4f}", "Abweichung_%": "{:+.1f} %"}),
                hide_index=True,
                use_container_width=True
            )
        else:
            st.success(f"Bei ±{threshold_pct}% Schwelle → keine Ausreißer gefunden")
    else:
        st.warning("Keine Daten für dieses Land.")

st.caption("Dashboard • Gaspreise EU Halbjahresdaten • Januar 2026")
