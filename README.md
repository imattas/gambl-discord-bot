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
---

### Running the bot

```bash
if [[ -d .git ]] && [[ "$GIT_PULL_CONDITION" == "1" ]]; then git pull; fi; if [[ ! -z "$PYTHON_PACKAGE" ]]; then pip install -U --prefix ~/.local "$PYTHON_PACKAGE"; fi; if [[ -f "/home/container/${REQUIREMENTS_FILE}" ]]; then pip install --disable-pip-version-check -U --prefix ~/.local -r "/home/container/${REQUIREMENTS_FILE}"; fi; if [[ ! -z "${START_BASH_FILE}" ]]; then bash "${START_BASH_FILE}"; else python3 /home/container/main.py; fi
```
```powershell
if (Test-Path ".git" -PathType Container -and $env:GIT_PULL_CONDITION -eq "1") { git pull }; if ($env:PYTHON_PACKAGE) { pip install --upgrade --prefix $HOME\.local $env:PYTHON_PACKAGE }; $reqFile = "C:\home\container\$env:REQUIREMENTS_FILE"; if (Test-Path $reqFile) { pip install --disable-pip-version-check --upgrade --prefix $HOME\.local -r $reqFile }; if ($env:START_BASH_FILE) { bash $env:START_BASH_FILE } else { python C:\home\container\main.py }
```
