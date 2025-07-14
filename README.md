# Gambl
**The ultimate way to gamble on Discord**

---

## Overview

**Gambl** is a Discord bot that brings a full-featured economy and gambling system to your server.  
Users can work, gamble, buy items from the shop, participate in heists, rob others, and level up.  
Includes admin commands, giveaways, and a welcoming system.

---

## Features

- Wallet and bank economy with deposit and withdrawal  
- Daily rewards and work to earn coins and XP  
- Gambling games: coinflip, roulette, slots, robbing other users  
- Heist system for group play  
- Shop and inventory system  
- XP and leveling with leaderboard  
- Giveaway system (role-restricted) with interactive buttons  
- Welcoming new members with a customizable embed  
- Admin commands for managing economy and shop  
- Role-based permission checks for sensitive commands

---

## Setup Instructions

### Requirements

- Python 3.8 or later  
- `discord.py` and dependencies (listed in `requirements.txt`)

### Installation

1. Clone or download this repository.  
2. Open your terminal or command prompt and navigate to the bot directory (where `requirements.txt` is located).  
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the bot

**Bash**
```bash
if [[ -d .git ]] && [[ "$GIT_PULL_CONDITION" == "1" ]]; then git pull; fi; if [[ ! -z "$PYTHON_PACKAGE" ]]; then pip install -U --prefix ~/.local "$PYTHON_PACKAGE"; fi; if [[ -f "/home/container/${REQUIREMENTS_FILE}" ]]; then pip install --disable-pip-version-check -U --prefix ~/.local -r "/home/container/${REQUIREMENTS_FILE}"; fi; if [[ ! -z "${START_BASH_FILE}" ]]; then bash "${START_BASH_FILE}"; else python3 /home/container/main.py; fi
```

**PowerShell**
```powershell
if (Test-Path ".git" -PathType Container -and $env:GIT_PULL_CONDITION -eq "1") { git pull }; if ($env:PYTHON_PACKAGE) { pip install --upgrade --prefix $HOME\.local $env:PYTHON_PACKAGE }; $reqFile = "C:\home\container\$env:REQUIREMENTS_FILE"; if (Test-Path $reqFile) { pip install --disable-pip-version-check --upgrade --prefix $HOME\.local -r $reqFile }; if ($env:START_BASH_FILE) { bash $env:START_BASH_FILE } else { python C:\home\container\main.py }
```

---

### Configuration
- The bot uses an SQLite database economy.db for persistent storage.
- Admin role ID is 1394342360158306325 (modify in code if needed).
- Giveaway role ID is 1394337905387897054 (only this role can start giveaways).
- Welcome messages are sent to channel ID 1394331213204033789 (change as appropriate).

---

## Commands

## Economy
**- `/balance` — Show your wallet and bank balance**
**- `/daily` — Claim daily coins**
**- `/work` — Work to earn coins and XP**
**- `/deposit <amount>` — Deposit coins into your bank**
**- `/withdraw <amount>` — Withdraw coins from your bank**
**- `/rank` — Show your level and XP**
**- `/leaderboard` — Top 10 richest users**

## Gambling
**- `/coinflip <heads|tails> <amount>` — Flip a coin to win or lose coins**
**- `/roulette <red|black|green> <amount>` — Bet on roulette colors**
**- `/slots <amount>` — Spin the slot machine**
**- `/rob <user>` — Attempt to rob another user**
**- `/heist` — Join a group heist (requires 3+ users)**

## Shop & Inventory

**- `/shop` — View shop items**
**- `/buy <item>` — Buy an item from the shop**
**- `/inventory` — Show your owned items**

## Admin
**- `/give <user> <amount>` — Give coins to a user (admin role required)**
**- `/setshop <item> <price>` — Add or update shop items (admin only)**

## Giveaways
**- `/giveaway <prize> <duration>` — Start a giveaway (role-restricted)
Participants enter via interactive buttons.**

---

## Bot Events
- Welcomes new members in the configured welcome channel with an embed message.

---

## Notes
**The bot uses slash commands (`/command`) and requires the bot to be invited with appropriate permissions.**
**Update role and channel IDs in the code to match your server setup.**
**Make sure the bot has permission to send messages, embed links, and manage messages if needed.**
**Keep your bot token secure and do not share it publicly.**

---

## License
This project is open source and free to use. Feel free to contribute or report issues.

---

## Contact
Create by imattas/zemi
Contact: [discord](https://discord.gg/gambl)

