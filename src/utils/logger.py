import logging
import os
from datetime import datetime
from pathlib import Path

import colorlog

# =====================================================================
# USER CONFIGURATION SWITCHES
# =====================================================================
WRITE_TO_FILE = False  # Set to False to stop creating log files
PRINT_TO_CONSOLE = True  # Set to False to silence the terminal output

LOG_LEVEL = logging.ERROR
LOG_APPLICATION_NAME = "Business Analysis"
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"

# --- Logger Base Setup ---
log = logging.getLogger(LOG_APPLICATION_NAME)
log.setLevel(LOG_LEVEL)
log.propagate = False  # Prevents duplicate logs in the console

# =====================================================================
# HANDLER INITIALIZATION (Controlled by switches above)
# =====================================================================

# 1. Conditional File Handler
if WRITE_TO_FILE:
    BASE_DIR = Path(os.getcwd()).resolve()
    LOG_DIRECTORY = BASE_DIR.parent / "bin" / "logs"
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    LOG_FILE_NAME = LOG_DIRECTORY / f"log-{LOG_APPLICATION_NAME.replace(' ', '_')}-{timestamp}.log"

    file_handler = logging.FileHandler(LOG_FILE_NAME, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    log.addHandler(file_handler)

# 2. Conditional Colorized Console Handler
if PRINT_TO_CONSOLE:
    COLOR_FORMAT = "%(log_color)s%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }

    color_formatter = colorlog.ColoredFormatter(
        COLOR_FORMAT,
        log_colors=LOG_COLORS,
        style='%'
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(color_formatter)
    log.addHandler(stream_handler)
