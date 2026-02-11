## Oppsett

Opprette virtual enviornment (venv)
```sh
python3 -m venv ./.venv
```

Aktivere virtual enviornment
```sh
source .venv/bin/activate
```

Installere krevde pakker
```sh
pip install -r requirements.txt
```

Lage ny dependency fil fra installerte pakker
```sh
pip freeze > requirements.txt
```
