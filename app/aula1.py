import requests

# Use o seu token real aqui
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjU4ZGJiZTg4LWVlMmQtNDFmMi1iYjViLTc4YWVmNjFjYWFlZiIsImlhdCI6MTc2ODg2NjY4NCwic3ViIjoiZGV2ZWxvcGVyLzJiZGJhYzMzLWU4YTYtYTgwZS01MWQxLWJhMjgxMDdiMzBiMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3OS4yMTIuMTQ5LjE2NiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.yeGXadiHJvN1VYc_E93fmnAf0jSQh3phlPKTF7PGJktT-FD9AbqM3fQhekfDDnEmnmqngigxGRi2fIcYc-aR6A"
tag = "%232R9VY2QYJ"
url = f"https://api.clashofclans.com/v1/clans/{tag}"
headers = {"Authorization": f"Bearer {token}"}

# Faz a requisição
resposta = requests.get(url, headers=headers)
dados = resposta.json()

# Imprimindo apenas o que nos interessa
# total_trofeus = 0
# for membro in dados['memberList']:
#     trofeus = membro['trophies']

#     total_trofeus = total_trofeus + trofeus

# print('-' * 30)
# print(f" total de trofeus do clan {total_trofeus}")
# print('-' * 30)

# max_doacoes = -1
# maior_doador = ""
# for membro in dados['memberList']:
#     nome = membro['name']
#     doou = membro['donations']

#     if doou > max_doacoes:
#         max_doacoes = doou
#         maior_doador = nome
# print(f"o maior doador eh o {maior_doador} com {max_doacoes}")

# min_townhall = 20
# menor_townhall = ""
# for membro in dados['memberList']:
#     nome = membro['name']
#     townhall = membro['townHallLevel']

#     if townhall < min_townhall:
#         min_townhall = townhall
#         menor_townhall = nome

# print(f"o menor centro de vila eh {min_townhall} do membro {menor_townhall}")

# Criamos um dicionário vazio
contagem_cvs = {}

for membro in dados['memberList']:
    cv = membro['townHallLevel']
    
    if cv in contagem_cvs:
        # Se a caixa do CV já existe, somamos +1 nela
        contagem_cvs[cv] += 1
    else:
        # Se é a primeira vez que vemos esse CV, criamos a caixa com 1
        contagem_cvs[cv] = 1

print("--- DISTRIBUIÇÃO DE CVS NO CLÃ ---")
print(contagem_cvs)
print("--- RELATÓRIO DE VILA ---")
# O .items() permite que o fiscal pegue a CHAVE e o VALOR ao mesmo tempo
for nivel, quantidade in contagem_cvs.items():
    print(f"Centro de Vila {nivel}: {quantidade} jogadores")

print("--- RELATÓRIO DE VILA ORDENADO ---")

# sorted() organiza as chaves (os níveis do CV)
# reverse=True faz com que comece do maior para o menor (16 -> 8)
for nivel in sorted(contagem_cvs.keys(), reverse=True):
    quantidade = contagem_cvs[nivel]
    print(f"Centro de Vila {nivel}: {quantidade} jogadores")