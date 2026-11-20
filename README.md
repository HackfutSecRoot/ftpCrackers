# 🔥 GHOST FTP CRACKER

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.8%2B-yellow?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

<p align="center">
  <b>⚡ Multi-Format FTP Credential Tester & Security Alert System ⚡</b><br>
  <i>Fast • Multi-Format • Telegram Alerts • Secure Domain Detection</i>
</p>

<p align="center">
  <a href="https://github.com/HackfutSecRoot/ftpCrackers"><img src="https://img.shields.io/badge/GitHub-HackfutSecRoot-black?style=for-the-badge&logo=github"></a>
  <a href="https://t.me/+gsrpvshwGUc5MzI0"><img src="https://img.shields.io/badge/Telegram-Channel_1-blue?style=for-the-badge&logo=telegram"></a>
  <a href="https://t.me/LinxProdXs404"><img src="https://img.shields.io/badge/Telegram-Channel_2-red?style=for-the-badge&logo=telegram"></a>
</p>

---

## 📖 Overview

**GHOST FTP CRACKER** is a powerful, multi-threaded FTP credential testing tool designed for security researchers and penetration testers. It automatically parses **9 different credential formats**, supports **high-speed multi-threaded checking**, and sends **real-time Telegram alerts** when high-security domains (`.gov`, `.edu`, `.mil`, etc.) are compromised.

> ⚠️ **Disclaimer:** This tool is provided for **educational and authorized security testing purposes only**. The author is **not responsible** for any misuse or illegal activity. Always obtain proper authorization before testing any system.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **9 Input Formats** | Supports `host:user:pass`, `url|user|pass`, `Host:... User:...`, and more |
| 🤖 **AUTO Mode** | Automatically detects & parses **all formats** in the same file |
| ⚡ **Fast Checker** | Multi-threaded engine (up to 50 workers) for blazing-fast testing |
| 🔔 **Telegram Alerts** | Instant notifications for successful logins on secure domains |
| 🛡️ **Secure Domain Detection** | Auto-detects `.gov`, `.edu`, `.gouv`, `.org`, `.mil`, `.int`, `gob`, `go` |
| 📁 **File Permission Grabbing** | Lists files & permissions on successful FTP login |
| 📝 **Dual Output** | Saves results to `Good_Ftp.txt` and `Bad_Ftp.txt` |
| 🎨 **Colorful CLI** | Rich terminal output with progress tracking |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/HackfutSecRoot/ftpCrackers.git
cd ftpCrackers

# Install dependencies
pip install requests rich pystyle
```

### Requirements
- **Python** 3.8+
- **pip** packages: `requests`, `rich`, `pystyle`

---

## ⚙️ Configuration

Before running, edit these lines in the script:

```python
# Replace with your Telegram Bot Token
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# Replace with your Chat ID or Group ID
CHAT_ID = 'YOUR_CHAT_ID_HERE'
```

### 🔑 How to get Telegram credentials:
1. Message [@BotFather](https://t.me/BotFather) → create a bot → copy the **token**
2. Message [@userinfobot](https://t.me/userinfobot) → copy your **chat ID**

---

## 🚀 Usage

```bash
python ftp_cracker.py
```

### Step-by-step:
1. **Choose input format** (1–9, or `9` for AUTO)
2. **Enter the path** to your credentials file
3. **Enable Fast Mode** (`y/n`)
4. *(If normal mode)* Provide an **optional password wordlist** for brute-forcing
5. **Watch results** in real-time with colored output

---

## 📋 Supported Formats

| # | Format | Example |
|---|--------|---------|
| 1 | `host:user:password` | `ftp.example.com:admin:pass123` |
| 2 | `host:user:password:port` | `ftp.example.com:admin:pass123:21` |
| 3 | `host - user;password - port` | `ftp.example.com - admin;pass123 - 21` |
| 4 | `ftp://hostname;user;pass` | `ftp://ftp.example.com;admin;pass123` |
| 5 | `Host: ... User: ... Password: ...` | `Host: ftp.example.com User: admin Password: pass123` |
| 6 | `url\|username\|password` | `ftp.example.com\|admin\|pass123` |
| 7 | `host:port:username:password` | `ftp.example.com:21:admin:pass123` |
| 8 | `host:port,user,password` | `ftp.example.com:21,admin,pass123` |
| 9 | **AUTO** | Detects & parses **all formats above** |

---

## 🎯 How It Works

```
┌──────────────────┐
│  Load Input File │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Parse Credentials│  ← 9 formats + AUTO detection
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Secure Domain?  │  ← .gov, .edu, .mil, etc.
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  FTP Login Test  │  ← Multi-threaded (Fast Mode)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Telegram Alert  │  ← Real-time notifications
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Save Results    │  ← Good_Ftp.txt / Bad_Ftp.txt
└──────────────────┘
```

---

## 🎨 Modes

### 🔹 Normal Mode
- Verifies FTP login
- Retrieves **file permissions** from the server
- Sends **detailed Telegram alerts**
- Saves results in `Good_Ftp.txt` and `Bad_Ftp.txt`

### 🔹 Fast Checker Mode
- Multi-threaded (up to **50 workers**)
- Skips permission grabbing for **maximum speed**
- Sends **lightweight Telegram alerts** on success
- Ideal for large credential lists

---

## 📊 Output Files

| File | Content |
|------|---------|
| `Good_Ftp.txt` | Valid FTP credentials |
| `Bad_Ftp.txt` | Invalid / failed credentials |

---

## 🔗 Links & Resources

### 📢 Telegram Channels
- **Channel 1** → [Join](https://t.me/+gsrpvshwGUc5MzI0)
- **Channel 2** → [Join](https://t.me/LinxProdXs404)
- **ULP Cloud** → `@ulp_CLOUD1`

### 📝 Posts
- [Post 1](https://t.me/LinxProdXs404/249)
- [Post 2](https://t.me/LinxProdXs404/541)

### 👤 Contact
- **GitHub** → [HackfutSecRoot](https://github.com/HackfutSecRoot/ftpCrackers)
- **Pastebin** → [pastebin.com/u/hackfut](https://pastebin.com/u/hackfut)
- **Telegram DM** → `@HackfutS3c`

---

## ⚠️ Legal Disclaimer

```
This tool is intended for AUTHORIZED SECURITY TESTING and EDUCATIONAL
purposes only. The author (@HackfutS3c) assumes NO responsibility for
any misuse, damage, or illegal activity caused by this software.

By using GHOST FTP CRACKER, you agree that:
  ✔ You have explicit permission to test the target systems
  ✔ You will comply with all applicable local and international laws
  ✔ You understand that unauthorized access is a criminal offense

Use responsibly. Stay ethical. 🛡️
```

---

## 📜 License

**MIT License** — see [LICENSE](https://github.com/HackfutSecRoot/ftpCrackers) for details.

---

<p align="center">
  <b>💀 Coded with passion by <a href="https://github.com/HackfutSecRoot">HackFut</a> 💀</b><br>
  <i>⭐ Star the repo if you find it useful! ⭐</i>
</p>
