import requests
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv("../.env")
TOKEN = os.getenv("COC_API_KEY")
TAG_CLAN = "#2R9VY2QYJ".replace('#', '%23')
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

conn = sqlite3.connect("../data/clash_history.db")

def atualizar_dados():
    url = f"https://api.clashofclans.com/v1/clans/{TAG_CLAN}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        dados = response.json()
        df = pd.json_normalize(dados['memberList'])

        df['coletado_em'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        colunas = ['coletado_em', 'name', 'tag', 'role', 'expLevel', 'trophies', 'donations', 'donationsReceived']
        df_final = df[colunas]

        df_final.to_sql('historico_membros', conn, if_exists='append', index=False)

        print(f"[{df['coletado_em'][0]} Dados de {len(df)} membros salvos no Banco de Dados]")
    else:
        print(f"Erro na API: {response.status_code}")

if __name__ == "__main__":
    atualizar_dados()
    conn.close()