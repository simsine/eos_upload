## Oppsett

### Opprette virtual environment (venv)

##### Linux

```sh
python3 -m venv ./.venv
```

##### Windows

```sh
python -m venv ./.venv
```

### Aktivere virtual environment

##### Linux

```sh
source .venv/bin/activate
```

##### Windows

```sh
# Command Prompt
.\venv\Scripts\activate

# PowerShell
.\venv\Scripts\Activate.ps1
```

### Installere krevde pakker

##### Linux og Windows

```sh
pip install -r requirements.txt
```

### Lage ny dependency-fil fra installerte pakker

##### Linux og Windows

```sh
pip freeze > requirements.txt
```
