

import analyzer_api.constants as cnst

from cast import settings

from pymongo import MongoClient

_db = MongoClient()[settings.DATABASE_NAME]

class AvailableLanguages(object):

    @staticmethod
    def check_lang_support(lang):        
        return lang in cnst.available_lang

    @staticmethod
    def to_json():
        return {
            'lang_list' : cnst.available_lang
        }

class AnalyzerModel(object):

    def __init__(self):                
        self._collection = _db[settings.COLLECTIONS['snippet_col']]

    def save_snippet(self,**kwargs):
        return self._collection.insert_one(kwargs)