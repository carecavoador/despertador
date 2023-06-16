import json
from pathlib import Path

ARQUIVO_CONFIG = Path().home().joinpath(".config/despertador.txt")


def carrega_config() -> dict:
    if not ARQUIVO_CONFIG.exists():
        salva_config(hora=12, minutos=30)
    config = json.load(Path(ARQUIVO_CONFIG).open(encoding="utf-8"))
    return config


def salva_config(
    hora: int,
    minutos: int,
) -> None:
    if not ARQUIVO_CONFIG.parent.exists():
        ARQUIVO_CONFIG.parent.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump({"hora": hora, "minutos": minutos}, f)
