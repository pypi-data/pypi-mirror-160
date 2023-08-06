import logging
from .bg import RemBg
logging.disable(logging.CRITICAL)

def set_logging(value=False):
    logging.disable(logging.NOTSET if value else logging.CRITICAL)