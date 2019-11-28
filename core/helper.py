import dotenv
from pathlib import Path


def load_env_file():
    env_path = Path('..') / '.env'
    dotenv.load_dotenv(dotenv_path=env_path)
