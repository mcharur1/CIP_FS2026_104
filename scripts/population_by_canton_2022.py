import requests
from pyjstat import pyjstat

# File URL provided by Federal Statistical Office
url = "https://www.pxweb.bfs.admin.ch/api/v1/en/px-x-0102020000_104/px-x-0102020000_104.px"

# JSON Query provided by Federal Statistical Office
query = {
    "query": [
        {"code": "Jahr", "selection": {"filter": "item", "values": ["2022"]}},
        {"code": "Kanton", "selection": {"filter": "item", "values": [str(i) for i in range(1, 28)]}},
        {"code": "Demografische Komponente", "selection": {"filter": "item", "values": ["14"]}}
    ],
    "response": {"format": "json-stat"}
}

response = requests.post(url, json=query)
dataset = pyjstat.Dataset.read(response.text)
df = dataset.write('dataframe')

# Change Canton naming to match Seda's
canton_map = {
    "Zürich": "zurich",
    "Bern / Berne": "berne",
    "Luzern": "lucerne",
    "Uri": "uri",
    "Schwyz": "schwyz",
    "Obwalden": "obwald",
    "Nidwalden": "nidwald",
    "Glarus": "glaris",
    "Zug": "zoug",
    "Fribourg / Freiburg": "fribourg",
    "Solothurn": "soleure",
    "Basel-Stadt": "bale-ville",
    "Basel-Landschaft": "bale-campagne",
    "Schaffhausen": "schaffhouse",
    "Appenzell Ausserrhoden": "appenzell-rhodes-exterieures",
    "Appenzell Innerrhoden": "appenzell-rhodes-interieures",
    "St. Gallen": "st-gall",
    "Graubünden / Grigioni / Grischun": "grisons",
    "Aargau": "argovie",
    "Thurgau": "thurgovie",
    "Ticino": "tessin",
    "Vaud": "vaud",
    "Valais / Wallis": "valais",
    "Neuchâtel": "neuchatel",
    "Genève": "geneva",
    "Jura": "jura"
}

df['Canton'] = df['Canton'].map(canton_map)
# Drop the "No jurisdiction" since it has 0 population
df = df.dropna(subset=['Canton'])
print(df)