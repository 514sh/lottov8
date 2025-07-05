from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime

load_dotenv()

OWNERS = os.environ.get("OWNERS").split(",")
KABO = os.environ.get("KABO").split(",")
base_dir_str = os.environ.get("BASE_DIR")
project_dir = os.environ.get("PROJECT_DIR")

if base_dir_str is None:
    raise EnvironmentError("BASE_DIR environment variable is not set.")

if project_dir is None:
    raise EnvironmentError("PROJECT_DIR environment variable is not set.")

BASE_DIR = Path(base_dir_str)
PROJECT_DIR = Path(project_dir)

GAME_DATE = datetime.now()

LIMIT = int(os.environ.get("LIMIT"))

static_folder = PROJECT_DIR / "lotto" / "static"

HEADER_FONT= str(static_folder / "RobotoMono-Thin.ttf")
BODY_FONT= str(static_folder / "RobotoMono-SemiBold.ttf")
