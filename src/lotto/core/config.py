from dotenv import load_dotenv
import os

load_dotenv()

OWNERS = os.environ.get("OWNERS").split(",")
BASE_PATH = os.environ.get("BASE_PATH")