import logging
import sys
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("neofactory")
logger.setLevel(logging.INFO)

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logHandler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(user_id)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
