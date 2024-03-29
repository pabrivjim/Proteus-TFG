# ==========================================================================
# File: i18n.py
# Description: Translator.
# Date: 04/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from os.path import join
import yaml
from PyQt5.QtCore import QSettings
import proteus
import proteus.config as config

CACHED_TRANS = None



def get_trans_dict(lang: str) -> dict:
    """
    Method that gets the traduction from the i18n files.
    """
    proteus.logger.info('i18n - get trans dict')
    global CACHED_TRANS
    if CACHED_TRANS is None:
        try:
            with open(join(config.Config().resources_directory, "i18n", lang) + ".yaml", encoding='utf8') as file:
                CACHED_TRANS = yaml.load(file, Loader=yaml.FullLoader)
        except (Exception,):
            CACHED_TRANS = {}

    return CACHED_TRANS


def trans(key: str) -> str:
    """
    Method that translate a string using the i18n files.
    """
    proteus.logger.info('i18n - trans')
    settings = QSettings("Proteus", "SettingsDesktop")
    language = settings.value("language", "es")
    # language = "es"  # settings.value("language", "es")
    return get_trans_dict(language).get(key, key)
