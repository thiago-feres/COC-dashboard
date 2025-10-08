import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# === CONFIGURAÇÕES ===
st.set_page_config(page_title="Clash of Clans - Dashboard", layout="wide")

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjcxZWYwOWM4LTgzNDUtNDc2MS04OGQ4LTZjOTAyYzdlNTJiZiIsImlhdCI6MTc1OTg5NDE0Niwic3ViIjoiZGV2ZWxvcGVyLzJiZGJhYzMzLWU4YTYtYTgwZS01MWQxLWJhMjgxMDdiMzBiMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3OS4yMTIuMTQ5LjE2NiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.QYgfu4XSDaJttyf5tpVe3NNA1uFrWXFmaKF8CpE6to1ABlcZjyGreFEc6zrlcW-s80URj5za66EPh7ozQNcWJg"
CLAN_TAG = "%232J9GV9YUL"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
HISTORY_FILE = "members_history.csv"

# === FUNÇÕES ===
@st.cache_data
def get_data(endpoint):
    url = f"https://api.clashofclans.com/v1{endpoint}"
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

        # Filtrar apenas as colunas que realmente existem
        cols_existentes = [c for c in ["tag", "name", "role", "expLevel", "trophies", "donations", "donationsReceived"] if c in df.columns]
        df = df[cols_existentes]

        # --- Carregar histórico anterior ---
        hist = load_member_history()
        today = datetime.now().strftime("%Y-%m-%d")

        # --- Detectar novos membros ---
        new_members = []
        for _, row in df.iterrows():
            if row["tag"] not in hist["tag"].values:
                new_members.append({"tag": row["tag"], "name": row.get("name", "Desconhecido"), "data_de_entrada": today})

        # --- Atualizar histórico ---
        updated_hist = pd.concat([hist, pd.DataFrame(new_members)], ignore_index=True).drop_duplicates("tag", keep="first")
        save_member_history(updated_hist)

        # --- Mesclar data de entrada ---
df = df.merge(updated_hist, on="tag", how="left")

# --- Garantir que existe uma coluna 'name' ---
if "name_x" in df.columns:
    df.rename(columns={"name_x": "name"}, inplace=True)
elif "name_y" in df.columns:
    df.rename(columns={"name_y": "name"}, inplace=True)

st.subheader("👥 Membros do Clã")
st.dataframe(df)

# --- Gráfico de doações ---
if "donations" in df.columns:
    st.markdown("### 📈 Ranking de Doações")
    fig = px.bar(df.sort_values("donations", ascending=False),
                 x="name", y="donations", color="role",
                 title="Doações por Jogador")
    st.plotly_chart(fig, use_container_width=True)


# === GUERRAS ===
with tabs[2]:
    if "items" in warlog:
        df_war = pd.DataFrame(warlog["items"])
        st.subheader("⚔️ Histórico de Guerras")
        st.dataframe(df_war[["result", "teamSize"]])

        # --- Contagem de resultados ---
        wins = df_war[df_war["result"] == "win"].shape[0]
        losses = df_war[df_war["result"] == "lose"].shape[0]
        draws = df_war[df_war["result"] == "tie"].shape[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Vitórias", wins)
        col2.metric("Derrotas", losses)
        col3.metric("Empates", draws)
    else:
        st.warning("Sem histórico de guerras disponível.")
