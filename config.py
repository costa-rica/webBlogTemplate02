import os
import json
from dotenv import load_dotenv

load_dotenv()


with open(os.path.join(os.environ.get('CONFIG_PATH'), os.environ.get('CONFIG_FILE_NAME'))) as config_file:
    config = json.load(config_file)


class ConfigBase:

    def __init__(self):

        self.SECRET_KEY = config.get('SECRET_KEY')
        # self.PROJ_ROOT_PATH = os.environ.get('PROJ_ROOT_PATH')
        # self.PROJ_DB_PATH = os.environ.get('PROJ_DB_PATH')
        # self.DESTINATION_PASSWORD = config.get('DESTINATION_PASSWORD')
        


class ConfigLocal(ConfigBase):

    def __init__(self):
        super().__init__()

    DEBUG = True
    SQL_URI = config.get('SQL_URI_LOCAL')
    WORD_DOC_DIR = config.get('WORD_DOC_DIR_LOCAL')
            

class ConfigDev(ConfigBase):

    def __init__(self):
        super().__init__()

    DEBUG = True
    SQL_URI = config.get('SQL_URI')
    WORD_DOC_DIR = config.get('WORD_DOC_DIR')
            

class ConfigProd(ConfigBase):

    def __init__(self):
        super().__init__()

    DEBUG = False
    SQL_URI = config.get('SQL_URI')
    WORD_DOC_DIR = config.get('WORD_DOC_DIR')

if os.environ.get('CONFIG_TYPE')=='local':
    config = ConfigLocal()
    print('- Personalwebsite/__init__: Development - Local')
elif os.environ.get('CONFIG_TYPE')=='dev':
    config = ConfigDev()
    print('- Personalwebsite/__init__: Development')
elif os.environ.get('CONFIG_TYPE')=='prod':
    config = ConfigProd()
    print('- Personalwebsite/__init__: Configured for Production')