import requests
import pandas as pd
import sqlite3
import os
import time 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv("../.env")
TOKEN = os.getenv("COC_API_KEY")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

conn = sqlite3.connect("../data/clash_history.db")

def atualizar_detalhes_jogadores():
    try:
        query = "SELECT DISTINCT tag FROM historico_membros"
        tags = pd.read_sql(query, conn)['tag'].tolist()
    except:
        print("A tabela historico_membros ainda nao existe. Rode o clan_sqlite3.py primeiro.")
        return

    detalhes = []
    print(f"Buscando detalhes de {len(tags)} jogadores...")

    for tag in tags:
        tag_url = tag.replace('#', '%23')
        try:

            res = requests.get(f"https://api.clashofclans.com/v1/players/{tag_url}", headers=HEADERS)

            if res.status_code == 200:
                p = res.json()

                herois = {h['name']: h['level'] for h in p.get('heroes', [])}
                tropas = {t['name']: t['level'] for t in p.get('troops', [])}
                feiticos = {s['name']: s['level'] for s in p.get('spells', [])}

                registro = {
                    'tag': p['tag'],
                    'townHallLevel': p.get('townHallLevel', 0),
                    'bestTrophies': p.get('bestTrophies', 0),
                    'warStars': p.get('warStars', 0),
                    'rei': herois.get('Barbarian King', 0),
                    'rainha': herois.get('Archer Queen', 0),
                    'principe_servo': herois.get('Minion Prince', 0),
                    'guardiao': herois.get('Grand Warden', 0),
                    'campea_real': herois.get('Royal Champion', 0),
                    'coletado_em': datetime.now().strftime("%d-%m-%Y %H:%M-%S")
                }

                for nome, nivel in tropas.items():
                    registro[f't_{nome}'] = nivel

                for nome, nivel in feiticos.items():
                    registro[f'f_{nome}'] = nivel
                
                detalhes.append(registro)
                print(f"OK: {p.get('name', tag)}")

            else:
                print(f"Erro na tag {tag}: Status {res.status_code}")

        except Exception as e:
            print(f"Erro ao processar {tag}: {e}")


        time.sleep(0.1)

    if detalhes:
        df_final = pd.DataFrame(detalhes)
        df_final.to_sql("player_details", conn, if_exists="replace", index=False)
        print("\nSucesso! Detalhes salvos na tabela 'player_details'.")
    conn.close()

if __name__ == "__main__":
    atualizar_detalhes_jogadores()
