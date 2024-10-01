# scripts/update_banner.py

import os
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import tweepy
from bs4 import BeautifulSoup
import random

# Function to get used Chains and check which have been used
def get_used_chains(file='chains_usadas.json'):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)  # Returns a list
    return []

def save_used_chain(chain, file='chains_usadas.json'):
    chains = get_used_chains(file)
    chains.append(chain)
    with open(file, 'w') as f:
        json.dump(chains, f)

def select_chain():
    response = requests.get('https://rpclist.com/chains')
    if response.status_code != 200:
        print("Error accessing the Chains page.")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    # Adjust the selector based on the actual site structure
    chains = [a['href'] for a in soup.select('a[href^="/chain/"]')]

    used_chains = get_used_chains()
    available_chains = [chain for chain in chains if chain not in used_chains]

    if not available_chains:
        print("All Chains have been used. Restarting the cycle.")
        # Restart the cycle by clearing the used Chains
        reset_cycle(file='chains_usadas.json')
        available_chains = chains  # All Chains are available again

    # Select the next available Chain in order
    for chain in chains:
        if chain not in used_chains:
            return chain

    # In case all Chains are used (after resetting)
    if available_chains:
        return available_chains[0]
    else:
        print("No Chains available to process.")
        return None

def reset_cycle(file='chains_usadas.json'):
    with open(file, 'w') as f:
        json.dump([], f)
    print("Cycle restarted. All Chains are available again.")

def extract_top5_providers(chain_url):
    response = requests.get(chain_url)
    if response.status_code != 200:
        print(f"Error accessing the Chain page: {chain_url}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    # Adjust the selector based on the actual site structure
    providers = [a.text.strip() for a in soup.select('a.provider-name')][:5]
    return providers

def generate_text(chain_name, providers, chain_url):
    # Templates for variation in informational paragraphs
    info_paragraphs = [
        f"These providers are offering outstanding performance, uptime, and speed on #{chain_name}!",
        f"Experience top-notch performance and reliability with these #RPC providers on #{chain_name}!",
        f"Enhance your #RPC experience on #{chain_name} with these leading providers!",
    ]

    highlight_paragraph = f"Major props to @{providers[0]} for leading the way with stellar performance! 🥇"

    incentive_paragraph = f"Check out {chain_url} and connect with these top-tier providers now!"

    # Randomly select a variation for the first paragraph
    info_paragraph = random.choice(info_paragraphs)

    text = f"""🔥 Top 5 RPC Providers on #{chain_name} Today!

1️⃣ @{providers[0]}

2️⃣ @{providers[1]}

3️⃣ @{providers[2]}

4️⃣ @{providers[3]}

5️⃣ @{providers[4]}

{info_paragraph}

{highlight_paragraph}

{incentive_paragraph}
"""
    return text

def post_to_x(text, image_path):
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    # Authenticate with the X API
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Post the image with the text
    try:
        api.update_with_media(image_path, status=text)
        print("Successfully posted to X.")
    except Exception as e:
        print(f"Error posting to X: {e}")

def main():
    chain = select_chain()
    if not chain:
        return

    chain_name = chain.split('/')[-1].replace('-', ' ').title()  # Example: "arbitrum-one" -> "Arbitrum One"
    chain_url = f"https://rpclist.com{chain}"
    top5 = extract_top5_providers(chain_url)
    if len(top5) < 5:
        print("Less than 5 providers found.")
        return

    text = generate_text(chain_name, top5, chain_url)
    post_to_x(text, 'assets/chains_captura.png')
    save_used_chain(chain)

if __name__ == "__main__":
    main()
