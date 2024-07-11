import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "font": [os.getenv('FONT_NAME'), os.getenv('FONT_SIZE')],
    'OBSIDIAN_DIR': os.getenv('OBSIDIAN_DIR'),
}
