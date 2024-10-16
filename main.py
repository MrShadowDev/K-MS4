import os
import re
import json
import asyncio
import aiohttp
import tkinter as tk
from tkinter import filedialog
import requests
import random

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    print("""

██╗  ██╗     ███╗   ███╗███████╗██╗  ██╗
██║ ██╔╝     ████╗ ████║██╔════╝██║  ██║
█████╔╝█████╗██╔████╔██║███████╗███████║
██╔═██╗╚════╝██║╚██╔╝██║╚════██║╚════██║
██║  ██╗     ██║ ╚═╝ ██║███████║     ██║
╚═╝  ╚═╝     ╚═╝     ╚═╝╚══════╝     ╚═╝
                                          
    """)

async def check_username_availability(session, username):
    url = f'https://keybase.io/_/api/1.0/user/lookup.json?username={username}'
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if 'them' not in data:
                return username, True  # Username is available
            elif 'status' in data and data['status']['code'] == 216:
                return username, False  # Username is deleted (unavailable)
            else:
                return username, False  # Username is taken
        return username, None  # API call failed

async def check_usernames_in_parallel(usernames, max_workers):
    available_usernames = []
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(max_workers)
        async def bounded_check(username):
            async with semaphore:
                return await check_username_availability(session, username)
        
        tasks = [bounded_check(username) for username in usernames]
        for response in await asyncio.gather(*tasks):
            username, available = response
            if available:
                available_usernames.append(username)
    return available_usernames

def remove_duplicates(usernames):
    valid_username_pattern = re.compile(r'^[\w]+$')
    return list(set(
        username for username in usernames
        if ' ' not in username and valid_username_pattern.match(username) and len(username) >= 4
    ))

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def get_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return file_path

def send_discord_message_with_file(webhook_url, message, file_path):
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        data = {'content': message}
        response = requests.post(webhook_url, data=data, files=files)
    return response.status_code == 200

def generate_random_words(count):
    url = f"https://random-word-api.herokuapp.com/word?number={count}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch random words. Using fallback method.")
        basic_words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]
        return random.choices(basic_words, k=count)

def main():
    clear_screen()
    print_ascii_art()
    
    config = load_config()
    choice = input("Choose an option:\n1. Check usernames from a file\n2. Generate random words\nEnter 1 or 2: ").strip()
    
    if choice == '1':
        input_file = get_file_path()
        if not input_file:
            print("No file selected. Exiting.")
            return
        with open(input_file, 'r', encoding='utf-8') as file:
            usernames = file.read().splitlines()
    elif choice == '2':
        word_count = int(input("Enter the number of random words to generate: "))
        usernames = generate_random_words(word_count)
    else:
        print("Invalid choice. Exiting.")
        return

    clear_screen()
    print_ascii_art()
    webhook_url = input("Enter Discord webhook URL: ").strip() or config.get('webhook_url', '')
    config['webhook_url'] = webhook_url
    max_workers = int(input("Enter number of workers (default 10): ") or config.get('max_workers', 10))
    config['max_workers'] = max_workers

    save_config(config)

    usernames = remove_duplicates(usernames)

    clear_screen()
    print_ascii_art()
    print("Checking usernames...")
    available_usernames = asyncio.run(check_usernames_in_parallel(usernames, max_workers))
    with open('availables.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(available_usernames))

    clear_screen()
    print_ascii_art()
    print(f"Found {len(available_usernames)} available usernames. Saved to availables.txt")
    if webhook_url:
        message = f"Found {len(available_usernames)} available usernames. Check the attached file for the list."
        if send_discord_message_with_file(webhook_url, message, 'availables.txt'):
            print("Notification and file sent to Discord successfully.")
        else:
            print("Failed to send notification and file to Discord.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()