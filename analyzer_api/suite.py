

import subprocess

import json

import random

import string

from analyzer_api import constants as cnst

numbers = [1,2,3,4,5,6,7,8,9,0]

class Response(object):

    def __init__(self):
        self.message_list = []
        self.error = ''
        self.status_code = 200

    def to_json(self):
        return {
            'status' : self.status_code,
            'error' : self.error,            
            'message' : self.message_list            
        }

class AnalyzeCodeAPI(object):

    def __init__(self, data = '',lang = '', file_name_len = 4):
        self.data = data
        
        self.file_name_len = file_name_len        
        
        self.temp_file = None

        self.lang = lang

        self.process_for_lang = cnst.get_func_for_lang[self.lang]

        self.resp = Response()

    def execute_arg(self,cmd): 
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)    
        return proc.communicate()

    def generate_file_id(self):
        return 'temp_' + ''.join( [ random.choice(string.ascii_lowercase) for i in range(self.file_name_len // 2) ] + \
                        [ str(random.choice(numbers)) for x in range(self.file_name_len // 2)  ] )

    def get_arg(self):
        self.temp_file = self.generate_file_id() + '.' + cnst.get_exec_for_language[self.lang]

        with open(self.temp_file,'w') as f:
            f.write(self.data)
        
        return cnst.get_arg_for_language[self.lang] % self.temp_file

    def analyze_file(self):

        output,error = self.execute_arg(self.get_arg())                
            
        if self.lang == 'c' or self.lang == 'cpp':
            self.resp.message_list = self.process_for_lang(error)

        else:
            self.resp.message_list = self.process_for_lang(output)
            self.resp.error = error.decode('ascii')
        
        self.remove_file()

        return self.resp.to_json()

    def remove_file(self):
        return self.execute_arg('rm %r' % self.temp_file)