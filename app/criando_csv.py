import requests
import csv
import os 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("COC_API_KEY")
TAG_ORIGINAL = "#2R9VY2QYJ"
TAG_URL = TAG_ORIGINAL.replace('#', '%23')
URL = f"https://api.clashofclans.com/v1/clans/{TAG_URL}"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
response = requests.get(URL, headers=HEADERS)
data_hoje = datetime.now().strftime('%Y-%m-%d')
print(f"Buscando dados do clan{TAG_ORIGINAL}...")
response = requests.get(URL, headers=HEADERS)
if response.status_code == 200:
    dados = response.json()
    nome_arquivo = "relatorio_focado.csv"
    colunas_importantes = ['name', 'role', 'townHallLevel', 'trophies', 'donations']

    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas_importantes, extrasaction='ignore')
        escritor.writeheader()
        escritor.writerows(dados['memberList'])

    print(f"✅ Arquivo historico gerado: {nome_arquivo}")
else:
    print(f"❌ Erro {response.status_code}: Verifique a Tag ou o Token.")