from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime

load_dotenv()

OWNERS = os.environ.get("OWNERS").split(",")
base_dir_str = os.environ.get("BASE_DIR")

if base_dir_str is None:
    raise EnvironmentError("BASE_DIR environment variable is not set.")

BASE_DIR = Path(base_dir_str)

GAME_DATE = datetime.now()