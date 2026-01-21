# 🛡️ Clash of Clans Clan Analytics

Este projeto em Python automatiza a extração de dados de clãs do Clash of Clans através da API oficial da Supercell, salvando as métricas dos membros em arquivos CSV para análise histórica.

## 🚀 Funcionalidades
- Busca automática de dados de membros via API.
- Armazenamento seguro de credenciais via variáveis de ambiente (`.env`).
- Geração de relatórios CSV com data e tag do clã no nome.
- Seleção inteligente de colunas (Nome, Nível, Troféus, Doações).

## 🛠️ Tecnologias Utilizadas
- **Python 3.12** (Gerenciado via `pyenv`)
- **Requests**: Para comunicação com a API.
- **Python-dotenv**: Para segurança de tokens.
- **CSV & Datetime**: Bibliotecas nativas para manipulação de dados.

## 📋 Como configurar
1. Obtenha sua API Key em [developer.clashofclans.com](https://developer.clashofclans.com).
2. Crie um arquivo `.env` na raiz do projeto:
   ```env
   COC_API_KEY=seu_token_aqui