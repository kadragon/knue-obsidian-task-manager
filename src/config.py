import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "font": ["Pretendard", 14],
    'OBSIDIAN_DIR': os.getenv('OBSIDIAN_DIR'),
}
