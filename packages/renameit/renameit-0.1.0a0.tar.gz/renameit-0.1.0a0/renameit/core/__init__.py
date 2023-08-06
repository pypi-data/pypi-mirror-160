import logging
import os

__version__ = "0.1.0-alpha.0"

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=LOGLEVEL,
    datefmt="%Y-%m-%d %I:%M:%S %p",
)
