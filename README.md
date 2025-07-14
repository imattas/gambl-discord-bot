# Gambl
**The ultimate way to gamble on discord**

# How to setup
**1. Install python 3.8 or Later**
**2. Open the directory with requirements.txt in it**
**3. Download the needed the requirements**
- run `pip install -r requirements.txt`
**4. Start the server for the bot**
- Linux/MaxOS (Bash Command):
`if [[ -d .git ]] && [[ "$GIT_PULL_CONDITION" == "1" ]]; then git pull; fi; if [[ ! -z "$PYTHON_PACKAGE" ]]; then pip install -U --prefix ~/.local "$PYTHON_PACKAGE"; fi; if [[ -f "/home/container/${REQUIREMENTS_FILE}" ]]; then pip install --disable-pip-version-check -U --prefix ~/.local -r "/home/container/${REQUIREMENTS_FILE}"; fi; if [[ ! -z "${START_BASH_FILE}" ]]; then bash "${START_BASH_FILE}"; else python3 /home/container/main.py; fi`
- Windows (Powershell Prompt)
`if (Test-Path ".git" -PathType Container -and $env:GIT_PULL_CONDITION -eq "1") { git pull }; if ($env:PYTHON_PACKAGE) { pip install --upgrade --prefix $HOME\.local $env:PYTHON_PACKAGE }; $reqFile = "C:\home\container\$env:REQUIREMENTS_FILE"; if (Test-Path $reqFile) { pip install --disable-pip-version-check --upgrade --prefix $HOME\.local -r $reqFile }; if ($env:START_BASH_FILE) { bash $env:START_BASH_FILE } else { python C:\home\container\main.py }`
