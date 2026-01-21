import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv("../.env")
TOKEN = os.getenv("COC_API_KEY")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

CLAN_TAG = "#2R9VY2QYJ".replace('#', '%23')
URL_CLAN = f"https://api.clashofclans.com/v1/clans/{CLAN_TAG}"

print("🚀 Iniciando extração completa...")

response_clan = requests.get(URL_CLAN, headers=HEADERS)
if response_clan.status_code == 200:
    membros = response_clan.json()['memberList']
    dados_completos = []

    for membro in membros:
        tag_player = membro['tag'].replace('#', '%23')
        print(f"  > Coletando detalhes de: {membro['name']}")
        
        # Chamada para o endpoint de PLAYER
        url_player = f"https://api.clashofclans.com/v1/players/{tag_player}"
        res_p = requests.get(url_player, headers=HEADERS)
        
        if res_p.status_code == 200:
            p = res_p.json()
            
            # Extraindo Heróis de uma forma segura (usando um mini-loop interno)
            herois = {h['name']: h['level'] for h in p.get('heroes', [])}
            
            # Criando o dicionário com as duas 'gavetas' unificadas
            registro = {
                'name': p['name'],
                'role': membro['role'], # Vem do clã
                'townHallLevel': p['townHallLevel'],
                'trophies': p['trophies'],
                'warStars': p.get('warStars', 0),
                'donations': p.get('donations', 0),
                'donationsReceived': p.get('donationsReceived', 0),
                'rei_nivel': herois.get('Barbarian King', 0),
                'rainha_nivel': herois.get('Archer Queen', 0),
                'guardiao_nivel': herois.get('Grand Warden', 0)
            }
            dados_completos.append(registro)
        
        # Pequena pausa para não ser bloqueado pela API por excesso de requisições
        time.sleep(0.05)

    # 4. Transformando em DataFrame final
    df_final = pd.DataFrame(dados_completos)
    
    # Salvando o Super Relatório
    caminho = "../data/relatorio_detalhado.csv"
    df_final.to_csv(caminho, index=False)
    print(f"\n✅ Super relatório gerado com sucesso em: {caminho}")

else:
    print("Erro ao acessar dados do clã.")