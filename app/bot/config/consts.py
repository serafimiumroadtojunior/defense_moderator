from pathlib import Path

BASE_DIR: Path = Path(__file__).parent.parent.parent
ENV_FILE: Path = BASE_DIR / '.env.example'
LOCALES_DIR: Path = BASE_DIR / 'bot' / 'locales'