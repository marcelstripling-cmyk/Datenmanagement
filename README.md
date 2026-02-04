
# Gaspreise EU Dashboard (2020–2025)

Interaktive Analyse der Gaspreise für Haushaltskunden (Eurostat nrg_pc_202) – in €/kWh

**Live:** https://datenmanagement-gaspreise.streamlit.app/  
**Repo:** https://github.com/marcelstripling-cmyk/Datenmanagement  
**Projekt:** Datenmanagement WS 2025/26

## Funktionen (4 Tabs)

- Preisverlauf pro Land (Linie + Min/Max)  
- Durchschnitt vs. Median (Balken + %)  
- Ausreißer-Analyse (Scatter + Schwellen-Slider)  
- Boxplot aller 24 Länder

## Start (lokal)

```bash
git clone https://github.com/marcelstripling-cmyk/Datenmanagement.git
cd Datenmanagement
pip install -r requirements.txt
streamlit run dashboard.py
```

## Technologien

- Python 3.10+  
- pandas  
- Streamlit  
- Plotly  
- Streamlit Cloud (Deployment)  
- Eurostat (Datenquelle)  
- Grok (xAI) – Code & Textunterstützung

## Hinweis

Erster Prototyp (Colab/matplotlib) verworfen – nur finale Streamlit-Version relevant.
