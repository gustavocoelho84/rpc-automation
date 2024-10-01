# scripts/update_banner.py

import os
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import tweepy
from bs4 import BeautifulSoup
import random

# Função para obter Chains e verificar quais já foram usadas
def obter_chains_usadas(arquivo='chains_usadas.json'):
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)  # Retorna uma lista
    return []

def salvar_chain_usada(chain, arquivo='chains_usadas.json'):
    chains = obter_chains_usadas(arquivo)
    chains.append(chain)
    with open(arquivo, 'w') as f:
        json.dump(chains, f)

def selecionar_chain():
    response = requests.get('https://rpclist.com/chains')
    if response.status_code != 200:
        print("Erro ao acessar a página de Chains.")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    # Ajuste o seletor conforme a estrutura real do site
    chains = [a['href'] for a in soup.select('a[href^="/chain/"]')]

    chains_usadas = obter_chains_usadas()
    chains_disponiveis = [chain for chain in chains if chain not in chains_usadas]

    if not chains_disponiveis:
        print("Todas as Chains já foram usadas. Reiniciando o ciclo.")
        # Reinicia o ciclo removendo todas as Chains usadas
        salvar_ciclo_reiniciado(arquivo='chains_usadas.json')
        chains_disponiveis = chains  # Todas as Chains estão disponíveis novamente

    # Seleciona a próxima Chain na ordem em que aparecem
    for chain in chains:
        if chain not in chains_usadas:
            return chain

    # Caso todas as Chains estejam usadas (após reiniciar)
    if chains_disponiveis:
        return chains_disponiveis[0]
    else:
        print("Nenhuma Chain disponível para processar.")
        return None

def salvar_ciclo_reiniciado(arquivo='chains_usadas.json'):
    with open(arquivo, 'w') as f:
        json.dump([], f)
    print("Ciclo reiniciado. Todas as Chains estão disponíveis novamente.")

def extrair_top5_providers(chain_url):
    response = requests.get(chain_url)
    if response.status_code != 200:
        print(f"Erro ao acessar a página da Chain: {chain_url}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    # Ajuste o seletor conforme a estrutura real do site
    providers = [a.text.strip() for a in soup.select('a.provider-name')][:5]
    return providers

def gerar_texto(chain_nome, providers, chain_url):
    # Templates para variação nos parágrafos informativos
    paragrafo_variacoes = [
        f"These providers are offering outstanding performance, uptime, and speed on #{chain_nome}!",
        f"Experience top-notch performance and reliability with these #RPC providers on #{chain_nome}!",
        f"Enhance your #RPC experience on #{chain_nome} with these leading providers!",
    ]

    paragrafo_destaque = f"Major props to @{providers[0]} for leading the way with stellar performance! 🥇"

    paragrafo_incentivo = f"Check out {chain_url} and connect with these top-tier providers now!"

    # Seleciona aleatoriamente uma variação para o primeiro parágrafo
    paragrafo_info = random.choice(paragrafo_variacoes)

    texto = f"""🔥 Top 5 RPC Providers on #{chain_nome} Today!

1️⃣ @{providers[0]}

2️⃣ @{providers[1]}

3️⃣ @{providers[2]}

4️⃣ @{providers[3]}

5️⃣ @{providers[4]}

{paragrafo_info}

{paragrafo_destaque}

{paragrafo_incentivo}
"""
    return texto

def postar_no_x(texto, imagem_path):
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    # Autenticação com a API do X
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Publicar a imagem com o texto
    try:
        api.update_with_media(imagem_path, status=texto)
        print("Postagem realizada com sucesso no X.")
    except Exception as e:
        print(f"Erro ao postar no X: {e}")

def main():
    chain = selecionar_chain()
    if not chain:
        return

    chain_nome = chain.split('/')[-1].replace('-', ' ').title()  # Exemplo: "arbitrum-one" -> "Arbitrum One"
    chain_url = f"https://rpclist.com{chain}"
    top5 = extrair_top5_providers(chain_url)
    if len(top5) < 5:
        print("Menos de 5 providers encontrados.")
        return

    texto = gerar_texto(chain_nome, top5, chain_url)
    postar_no_x(texto, 'assets/chains_captura.png')
    salvar_chain_usada(chain)

if __name__ == "__main__":
    main()
