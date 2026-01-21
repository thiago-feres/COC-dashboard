import streamlit as st
import requests
import pandas as pd

st.title("🛡️ Clan Analytics")

# FUNÇÃO DE BUSCA (Ajustada para segurança)
def get_clan_data(tag):
    token = st.secrets["COC_API_KEY"]
    tag = tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{tag}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

# COLOQUE A TAG AQUI (Certifique-se que o clã tem membros!)
CLAN_TAG = "#2R9VY2QYJ"

dados = get_clan_data(CLAN_TAG)

if dados:
    st.header(f"Clã: {dados.get('name')}")
    
    # SÓ ENTRA AQUI SE TIVER MEMBROS
    if 'memberList' in dados and len(dados['memberList']) > 0:
        df = pd.DataFrame(dados['memberList'])
        
        # Métricas
        m1, m2 = st.columns(2)
        m1.metric("Membros", len(df))
        m2.metric("Pontos", dados.get('clanPoints'))

        # GRÁFICO (Protegido contra erro de coluna)
        st.subheader("📊 Ranking de Doações")
        if 'name' in df.columns:
            # Criamos um resumo para o gráfico não ficar gigante
            chart_data = df[['name', 'donations']].set_index('name')
            st.bar_chart(chart_data)
        
        st.write("### Tabela de Membros", df)
    else:
        st.error("⚠️ Este clã foi encontrado, mas a lista de membros está vazia!")
        st.info("Dica: Tente usar a tag de um clã ativo (ex: #2PP92L2GV) para testar o gráfico.")
else:
    st.error("❌ Não foi possível conectar. Verifique o Token ou a TAG.")