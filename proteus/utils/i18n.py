from os.path import join, dirname
import yaml
# from PyQt5.QtCore import QSettings
import logging

CACHED_TRANS = None
CURRENT_FOLDER = dirname(dirname(__file__))
CONFIG_FOLDER = join(CURRENT_FOLDER, 'resources/config')


def get_trans_dict(lang: str) -> dict:
    """
    Method that gets the traduction from the i18n files.
    """
    logging.info('i18n - get trans dict')
    global CACHED_TRANS
    if CACHED_TRANS is None:
        try:
            with open(join(CONFIG_FOLDER, "i18n", lang) + ".yaml", encoding='utf8') as file:
                CACHED_TRANS = yaml.load(file, Loader=yaml.FullLoader)
        except (Exception,):
            CACHED_TRANS = {}

    return CACHED_TRANS


def trans(key: str) -> str:
    """
    Method that translate a string using the i18n files.
    """
    logging.info('i18n - trans')
    # settings = QSettings("Proteus", "SettingsDesktop")
    language = "es"  # settings.value("language", "es")
    return get_trans_dict(language).get(key, key)
