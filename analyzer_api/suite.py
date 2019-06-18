import subprocess

import json

import random

import string

import datetime 

from analyzer_api import constants as cnst

from analyzer_api.models import AnalyzerModel, AvailableLanguages

class ApiResponse(object):

    def __init__(self):
        self.message_list = []
        self.error = []
        self.status_code = 200

    def to_json(self):
        return {
            'status' : self.status_code,
            'error' : self.error,            
            'message' : self.message_list            
        }

class AnalyzeCodeAPI(ApiResponse,AnalyzerModel):

    def __init__(self, data = '',lang = '', file_name_len = 4, valid = True):
                
        self.is_valid = valid

        self.data = data
        
        self.file_name_len = file_name_len        
        
        self.temp_file = None

        self.lang = lang

        self.process_for_lang = cnst.get_func_for_lang[self.lang]

        ApiResponse.__init__(self)

        AnalyzerModel.__init__(self)

    def __call__(self):        
        return self.analyze_file()

    def __new__(cls,*args,**kwargs):                
        
        if not AvailableLanguages.check_lang_support(kwargs['lang']):            
            resp = ApiResponse()
            resp.error.append('Lang %s not supported' % (kwargs['lang']))
            resp.status_code = 400
            kwargs['valid'] = False
            return resp.to_json()

        elif not kwargs['data'] or len(kwargs['data'].strip()) == 0:
            resp = ApiResponse()
            resp.error.append('Data cannot be an empty string')
            resp.status_code = 400
            kwargs['valid'] = False
            return resp.to_json()                     
        
        return super(AnalyzeCodeAPI,cls).__new__(cls)        

    def execute_arg(self,cmd): 
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)    
        return proc.communicate()

    def generate_file_id(self):
        return 'temp_' + ''.join( [ random.choice(string.ascii_lowercase) for i in range(self.file_name_len // 2) ] + \
                        [ str(random.choice(cnst.numbers)) for x in range(self.file_name_len // 2)  ] )

    def get_arg(self):
        self.temp_file = self.generate_file_id() + '.' + cnst.get_exec_for_language[self.lang]

        with open(self.temp_file,'w') as f:
            f.write(self.data)
        
        return cnst.get_arg_for_language[self.lang] % self.temp_file

    def analyze_file(self):

        output,error = self.execute_arg(self.get_arg())                
            
        if self.lang == 'c' or self.lang == 'cpp':
            self.message_list = self.process_for_lang(error)

        else:
            self.message_list = self.process_for_lang(output)
            self.error.append(error.decode('ascii'))
        
        self.remove_file()

        self.save_snippet(
            lang = self.lang,
            name = self.temp_file,
            created_date = datetime.datetime.utcnow(),
            data = self.data
        )

        return self.to_json()

    def remove_file(self):
        return self.execute_arg('rm %r' % self.temp_file)