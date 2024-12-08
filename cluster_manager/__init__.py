__version__ = "0.0.1"

import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s %(levelname)s %(filename)s: %(message)s'
)
