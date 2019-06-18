

import analyzer_api.constants as cnst

class AvailableLanguages(object):

    @staticmethod
    def to_json():
        return {
            'lang_list' : cnst.available_lang
        }