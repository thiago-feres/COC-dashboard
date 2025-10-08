import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import os

# === CONFIGURAÇÕES ===
st.set_page_config(page_title="Clash of Clans - Dashboard", layout="wide")

# === VARIÁVEIS DE AMBIENTE ===

TOKEN = os.environ.get("ROYAL_API_TOKEN")
CLAN_TAG = os.environ.get("CLAN_TAG")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
HISTORY_FILE = "members_history.csv"

# === FUNÇÕES ===
@st.cache_data
def get_data(endpoint):
    url = f"https://proxy.royaleapi.dev/v1{endpoint}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        st.warning(f"Erro {r.status_code} em {endpoint}: {r.text}")
        return {}

def load_member_history():
    try:
        return pd.read_csv(HISTORY_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["tag", "name", "join_date"])

def save_member_history(df):
    df.to_csv(HISTORY_FILE, index=False)

# === COLETA DE DADOS ===
clan = get_data(f"/clans/{CLAN_TAG.replace('#', '%23')}")
members = get_data(f"/clans/{CLAN_TAG.replace('#', '%23')}/members")
warlog = get_data(f"/clans/{CLAN_TAG.replace('#', '%23')}/warlog")

# === INTERFACE ===
st.title("🏰 Dashboard - Clash of Clans")
st.markdown("---")
tabs = st.tabs(["🏡 Clã", "👥 Membros", "⚔️ Guerras"])

# === CLÃ ===
with tabs[0]:
    if clan:
        col1, col2 = st.columns(2)
        with col1:
            st.header(clan["name"])
            st.subheader(f"Tag: {clan['tag']}")
            st.write(f"Descrição: {clan.get('description', 'Sem descrição.')}")
        with col2:
            st.metric("Nível do Clã", clan["clanLevel"])
            st.metric("Pontos do Clã", clan["clanPoints"])
            st.metric("Membros", clan["members"])
    else:
        st.error("Não foi possível carregar os dados do clã.")

# === MEMBROS ===
with tabs[1]:
    if "items" in members and len(members["items"]) > 0:
        df = pd.DataFrame(members["items"])

        # Filtrar apenas as colunas existentes
        cols_existentes = [c for c in ["tag", "name", "role", "expLevel", "trophies", "donations", "donationsReceived"] if c in df.columns]
        df = df[cols_existentes]

        # --- Histórico de membros ---
        hist = load_member_history()
        today = datetime.now().strftime("%Y-%m-%d")

        # Detectar novos membros
        new_members = []
        for _, row in df.iterrows():
            if row["tag"] not in hist["tag"].values:
                new_members.append({
                    "tag": row["tag"],
                    "name": row.get("name", "Desconhecido"),
                    "join_date": today
                })

        # Atualizar histórico
        updated_hist = pd.concat([hist, pd.DataFrame(new_members)], ignore_index=True).drop_duplicates("tag", keep="first")
        save_member_history(updated_hist)

        # Mesclar data de entrada
        df = df.merge(updated_hist, on="tag", how="left")

        # Garantir que exista uma coluna 'name' para o gráfico
        if "name_x" in df.columns:
            df.rename(columns={"name_x": "name"}, inplace=True)
        elif "name_y" in df.columns:
            df.rename(columns={"name_y": "name"}, inplace=True)

        st.subheader("👥 Membros do Clã")
        st.dataframe(df)

        # --- Gráfico de doações ---
        if "donations" in df.columns:
            st.markdown("### 📈 Ranking de Doações")
            fig = px.bar(
                df.sort_values("donations", ascending=False),
                x="name",
                y="donations",
                color="role",
                title="Doações por Jogador"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Novos membros detectados
        if new_members:
            st.success(f"🎉 {len(new_members)} novo(s) membro(s) detectado(s) hoje!")
            st.table(pd.DataFrame(new_members)[["name", "join_date"]])

    else:
        st.error("Nenhum membro encontrado ou resposta vazia da API.")

# === GUERRAS ===
with tabs[2]:
    if warlog.get("items"):
        df_war = pd.DataFrame(warlog["items"])
        st.subheader("⚔️ Histórico de Guerras")
        st.dataframe(df_war[["result", "teamSize"]])

        # Contagem de resultados
        wins = df_war[df_war["result"] == "win"].shape[0]
        losses = df_war[df_war["result"] == "lose"].shape[0]
        draws = df_war[df_war["result"] == "tie"].shape[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Vitórias", wins)
        col2.metric("Derrotas", losses)
        col3.metric("Empates", draws)
    else:
        st.warning("Sem histórico de guerras disponível ou token sem permissão.")
