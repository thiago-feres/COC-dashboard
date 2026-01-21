import requests
import pandas as pd
import os 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv("../.env")
TOKEN = os.getenv("COC_API_KEY")
TAG_ORIGINAL = "#2R9VY2QYJ"
TAG_URL = TAG_ORIGINAL.replace('#', '%23')
URL = f"https://api.clashofclans.com/v1/clans/{TAG_URL}"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

print(f"Buscando dados do clan{TAG_ORIGINAL}...")
response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    dados = response.json()

    df = pd.json_normalize(dados['memberList'])
    colunas_finais = [
        'name', 'role', 'townHallLevel', 'trophies', 'donations', 'donationsReceived'
    ]

    df_filtrado = df[colunas_finais]
    data_hoje = datetime.now().strftime('%d-%m-%Y')
    tag_limpa = TAG_ORIGINAL.replace("#", "")
    nome_arquivo = f"../data/relatorio_{tag_limpa}_{data_hoje}.csv"
    df_filtrado.to_csv(nome_arquivo, index=False, encoding='utf-8')

    print(f"✅ Arquivo historico gerado: {nome_arquivo}")
    print(f"📊 Total de membros processados: {len(df_filtrado)}")
else:
    print(f"❌ Erro {response.status_code}: Verifique a Tag ou o Token.")