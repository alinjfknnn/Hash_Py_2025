import hashlib
import os
import time
import random
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


THEMES = {
    "dark": {
        "title": Fore.CYAN + Style.BRIGHT,
        "text": Fore.WHITE,
        "accent": Fore.MAGENTA,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "info": Fore.YELLOW,
    },
    "light": {
        "title": Fore.BLUE + Style.BRIGHT,
        "text": Fore.BLACK,
        "accent": Fore.MAGENTA,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "info": Fore.CYAN,
    }
}
user_theme = "dark"


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.02):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def progress_bar(duration=0.8):
    color = THEMES[user_theme]["accent"]
    print(color + "Hashing in progress ", end="", flush=True)
    for _ in range(15):
        print(color + "█", end="", flush=True)
        time.sleep(duration / 15)
    print(f" {THEMES[user_theme]['success']}Done!{Style.RESET_ALL}\n")

def safe_input(prompt, valid=None, lowercase=True):
    val = input(prompt).strip()
    if lowercase:
        val = val.lower()
    if valid and val not in valid:
        print(f"{THEMES[user_theme]['error']}⚠ Invalid choice!{Style.RESET_ALL}")
        return None
    return val


def generate_hash(text, algorithm):
    try:
        encoded = text.encode()
        return getattr(hashlib, algorithm)(encoded).hexdigest()
    except AttributeError:
        return None

def multi_hash(text):
    return {
        "MD5": hashlib.md5(text.encode()).hexdigest(),
        "SHA1": hashlib.sha1(text.encode()).hexdigest(),
        "SHA256": hashlib.sha256(text.encode()).hexdigest(),
        "SHA512": hashlib.sha512(text.encode()).hexdigest(),
    }

def verify_hash(text, given_hash, algorithm):
    try:
        return generate_hash(text, algorithm) == given_hash
    except Exception:
        return False

def save_to_file(text, data, filename=None):
    if not filename:
        filename = "hash_py_output.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}]\nText: {text}\n")
        for algo, val in data.items():
            f.write(f"{algo:<8}: {val}\n")
        f.write("-" * 60 + "\n")
    print(f"{THEMES[user_theme]['success']}✔ Output saved to {filename}{Style.RESET_ALL}")


def print_banner():
    color = THEMES[user_theme]["title"]
    quotes = [
        "“Security is not a product, but a process.” – Bruce Schneier",
        "“The quieter you become, the more you can hear.” – Ram Dass",
        "“Hash it before they hack it.” – Unknown",
        "“Encryption is freedom in code.” – Anonymous",
    ]
    quote = random.choice(quotes)
    clear()
    print(f"""
{color}
╔══════════════════════════════════════════════════════════╗
║                         ⚡ HASH_PY ⚡                    ║
║                    Ultimate Edition v1.0.0               ║
╠══════════════════════════════════════════════════════════╣
║  Author   : a.v in github is alinjfknnn                  ║
║  Modes    : Dark / Light                                 ║
║  Hashes   : SHA256 | SHA512 | SHA1 | MD5    
╚══════════════════════════════════════════════════════════╝
{THEMES[user_theme]['info']}{quote}{Style.RESET_ALL}
""")

def theme_selector():
    global user_theme
    print(f"{Fore.YELLOW}Select theme ↓{Style.RESET_ALL}")
    print("[1] Dark Mode")
    print("[2] Light Mode")
    choice = input("> ").strip()
    user_theme = "light" if choice == "2" else "dark"

def main_menu():
    print(f"{THEMES[user_theme]['success']}Welcome to Hash_Py, your secure & stylish hashing companion.{Style.RESET_ALL}")
    print("Choose your mission:\n")
    print(f"{THEMES[user_theme]['accent']}[1]{Style.RESET_ALL} Create a single hash")
    print(f"{THEMES[user_theme]['accent']}[2]{Style.RESET_ALL} Generate all hash types")
    print(f"{THEMES[user_theme]['accent']}[3]{Style.RESET_ALL} Verify a hash")
    print(f"{THEMES[user_theme]['accent']}[4]{Style.RESET_ALL} Change Theme")
    print(f"{THEMES[user_theme]['accent']}[5]{Style.RESET_ALL} About")
    print(f"{THEMES[user_theme]['accent']}[6]{Style.RESET_ALL} Exit\n")
    return safe_input(f"{THEMES[user_theme]['info']}Your choice → {Style.RESET_ALL}", valid=["1","2","3","4","5","6"])


def main():
    theme_selector()
    while True:
        clear()
        print_banner()
        choice = main_menu()

        if choice == "1":
            text = input(f"\n{THEMES[user_theme]['info']}Enter text to hash: {Style.RESET_ALL}")
            algorithm = safe_input(f"{THEMES[user_theme]['accent']}Algorithm (sha256 / sha512 / sha1 / md5): {Style.RESET_ALL}",
                                   valid=["sha256","sha512","sha1","md5"])
            if not algorithm: 
                time.sleep(1.5)
                continue

            progress_bar()
            start = time.perf_counter()
            hashed = generate_hash(text, algorithm)
            duration = round(time.perf_counter() - start, 5)

            print(f"\n{THEMES[user_theme]['success']}✔ Hash Generated Successfully!")
            print(f"{THEMES[user_theme]['info']}Algorithm:{Style.RESET_ALL} {algorithm.upper()}")
            print(f"{THEMES[user_theme]['info']}Hash:{Style.RESET_ALL} {hashed}")
            print(f"{THEMES[user_theme]['info']}Time:{Style.RESET_ALL} {duration}s")

            save = safe_input(f"\n{THEMES[user_theme]['accent']}Save to file? (y/n): {Style.RESET_ALL}", valid=["y","n"])
            if save == "y":
                name = input(f"{THEMES[user_theme]['info']}Enter filename (leave empty for default): {Style.RESET_ALL}").strip()
                save_to_file(text, {algorithm.upper(): hashed}, name or None)
            input(f"\n{THEMES[user_theme]['accent']}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "2":
            text = input(f"\n{THEMES[user_theme]['info']}Enter text to hash: {Style.RESET_ALL}")
            progress_bar()
            start = time.perf_counter()
            hashes = multi_hash(text)
            duration = round(time.perf_counter() - start, 5)

            print(f"\n{THEMES[user_theme]['success']}All Hashes Generated ↓")
            for algo, h in hashes.items():
                print(f"{THEMES[user_theme]['info']}{algo:<8}{Style.RESET_ALL}: {h}")
            print(f"\n⏱ Time taken: {duration}s")

            save = safe_input(f"\n{THEMES[user_theme]['accent']}Save to file? (y/n): {Style.RESET_ALL}", valid=["y","n"])
            if save == "y":
                name = input(f"{THEMES[user_theme]['info']}Enter filename (leave empty for default): {Style.RESET_ALL}").strip()
                save_to_file(text, hashes, name or None)
            input(f"\n{THEMES[user_theme]['accent']}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "3":
            text = input(f"\n{THEMES[user_theme]['info']}Enter original text: {Style.RESET_ALL}")
            algorithm = safe_input(f"{THEMES[user_theme]['accent']}Algorithm used (sha256 / sha512 / sha1 / md5): {Style.RESET_ALL}",
                                   valid=["sha256","sha512","sha1","md5"])
            if not algorithm:
                continue
            given_hash = input(f"{THEMES[user_theme]['info']}Enter hash to verify: {Style.RESET_ALL}")

            progress_bar(0.6)
            result = verify_hash(text, given_hash, algorithm)
            if result:
                print(f"{THEMES[user_theme]['success']}✅ Verified! The hash matches perfectly.{Style.RESET_ALL}")
            else:
                print(f"{THEMES[user_theme]['error']}❌ Verification failed. Hashes don’t match.{Style.RESET_ALL}")
            input(f"\n{THEMES[user_theme]['accent']}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == "4":
            theme_selector()
            continue

        elif choice == "5":
            print_banner()
            slow_print(f"{THEMES[user_theme]['info']}Hash_Py is your comfortable yet powerful hashing lab.", 0.03)
            slow_print("Built for coders who love clean design and secure logic.", 0.03)
            slow_print("Created by Ali — where simplicity meets power ⚡", 0.03)
            input(f"\n{THEMES[user_theme]['accent']}Press Enter to return...{Style.RESET_ALL}")

        elif choice == "6":
            clear()
            slow_print(f"{THEMES[user_theme]['accent']}Shutting down Hash_Py...", 0.03)
            slow_print(f"{THEMES[user_theme]['success']}Goodbye, Guardian of Hashes 👋{Style.RESET_ALL}", 0.03)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program interrupted by user. Exiting safely...{Style.RESET_ALL}")
        time.sleep(1)