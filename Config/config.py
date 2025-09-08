import os
from pathlib import Path

# Try to load .env if python-dotenv is available; ignore if missing
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = os.getenv("IMAGES_DIR", "images")
LOGO_IMG = os.getenv("LOGO_IMG", "aa-120x120.webp")
USER_ICON = os.getenv("USER_ICON", "user.png")
REPORT_ICON = os.getenv("REPORT_ICON", "report.png")
SETTINGS_ICON = os.getenv("SETTINGS_ICON", "settings.png")
BACK_ICON = os.getenv("BACK_ICON", "left-arrow (1).png")


def _image_path(file_name: str) -> str:
    return str((BASE_DIR / IMAGES_DIR / file_name).resolve())


LOGO_PATH = _image_path(LOGO_IMG)
USER_ICON_PATH = _image_path(USER_ICON)
REPORT_ICON_PATH = _image_path(REPORT_ICON)
SETTINGS_ICON_PATH = _image_path(SETTINGS_ICON)
BACK_ICON_PATH = _image_path(BACK_ICON)

# -------- Serial defaults (centralized) --------
# Allow overriding via environment variables.
DEFAULT_SERIAL_PORT = os.getenv("SERIAL_PORT", "COM4")
DEFAULT_SERIAL_BAUDRATE = int(os.getenv("SERIAL_BAUDRATE", "115200"))
DEFAULT_SERIAL_TIMEOUT = float(os.getenv("SERIAL_TIMEOUT", "0.1"))
DEFAULT_SERIAL_COMMAND = os.getenv("SERIAL_COMMAND", "RAI01;")
DEFAULT_SERIAL_DELAY_SECONDS = float(os.getenv("SERIAL_DELAY_SECONDS", "0.1"))