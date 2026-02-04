import sys
import os
from dotenv import load_dotenv, find_dotenv



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_ROOT)

load_dotenv(find_dotenv())
DATABASE_URL = os.getenv("DATABASE_URL")

print(BASE_DIR)
print(PROJECT_ROOT)
print(DATABASE_URL)