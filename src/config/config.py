import logging
import os

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(format="%(asctime)s |%(name)s| %(levelname)s: %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# MYSQL
MYSQL_DATABASE = os.environ.get('MYSQL_DB')
MYSQL_DATABASE_DW = os.environ.get('MYSQL_DB_DW')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_PORT = os.environ.get('MYSQL_PORT')
MYSQL_HOST = os.environ.get('MYSQL_HOST')



def load():
    log.info('Loading settings...')
    required_env_vars = [
        'MYSQL_DATABASE',
        'MYSQL_USER',
        'MYSQL_PASSWORD',
        'MYSQL_PORT',
        'MYSQL_HOST',
        'MYSQL_DATABASE_DW',
    ]

    for env_var in required_env_vars:
        if env_var not in os.environ:
            raise EnvironmentError(f'Environment variable not founded.')