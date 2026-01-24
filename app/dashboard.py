import streamlit as st
import sqlite3
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Análise do Clã - Clash of Clans", layout="wide")

# 1. Função para carregar os dados
def carregar_dados():
    conn = sqlite3.connect("../data/clash_history.db")
    query = """
    SELECT 
        h.*, 
        p.*
    FROM historico_membros h
    LEFT JOIN player_details p ON h.tag = p.tag
    ORDER BY h.coletado_em DESC
    """
    df = pd.read_sql(query, conn)
    # Remove colunas duplicadas (como a tag que vem das duas tabelas)
    df = df.loc[:, ~df.columns.duplicated()]
    conn.close()
    return df

# Execução inicial
st.title("🛡️ Dashboard de Evolução do Clã")
df = carregar_dados()

# 2. Barra Lateral (Filtros Gerais)
st.sidebar.header("Filtros de Centro de Vila")
th_selecionados = st.sidebar.multiselect(
    "Filtrar por TH:",
    options=sorted(df['townHallLevel'].unique()),
    default=sorted(df['townHallLevel'].unique())
)

df_filtrado = df[df['townHallLevel'].isin(th_selecionados)]

# 3. Métricas Principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Membros", len(df_filtrado))
col2.metric("Média de Troféus", int(df_filtrado['trophies'].mean()) if not df_filtrado.empty else 0)
col3.metric("Média de TH", round(df_filtrado['townHallLevel'].mean(), 1) if not df_filtrado.empty else 0)

st.divider()

# --- NOVIDADE: SELETOR DINÂMICO DE TROPAS ---
st.subheader("🔍 Consultar Nível de Tropa Específica")

# Identifica todas as colunas que são tropas (começam com t_)
lista_tropas = [col for col in df.columns if col.startswith('t_')]
# Remove o prefixo 't_' apenas para exibição no seletor
nomes_tropas_limpos = [t.replace('t_', '') for t in lista_tropas]

col_sel, col_vazia = st.columns([1, 2])
with col_sel:
    tropa_escolhida_nome = st.selectbox("Escolha a Tropa:", options=sorted(nomes_tropas_limpos))

# Volta o prefixo para buscar no DataFrame
tropa_real = f"t_{tropa_escolhida_nome}"

# Filtra apenas jogadores que possuem a tropa (nível > 0)
df_tropa = df_filtrado[df_filtrado[tropa_real] > 0][['name', 'townHallLevel', tropa_real]]
df_tropa = df_tropa.sort_values(by=tropa_real, ascending=False)

# Exibe a tabela formatada
st.dataframe(
    df_tropa.rename(columns={tropa_real: "Nível da Tropa", "name": "Jogador", "townHallLevel": "TH"}),
    use_container_width=True,
    hide_index=True
)
# --------------------------------------------

st.divider()

# 4. Gráfico de Heróis
st.subheader("⚔️ Nível dos Heróis por Jogador")
st.bar_chart(df_filtrado.set_index('name')[['rei', 'rainha', 'guardiao', 'campea_real']])

# 5. Tabela Geral
st.subheader("📊 Tabela Geral de Dados")
st.dataframe(df_filtrado)