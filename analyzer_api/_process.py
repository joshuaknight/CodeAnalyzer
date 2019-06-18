
import json


def data_for_python(output):
    return output.decode('ascii').strip().split('\n')

def data_for_html(output):
    try:           
        return [ msg['message'] for msg in json.loads(output)[0]['messages'] ]
    except:
        pass
    return []

def data_for_javascript(output):    
    return output.decode('ascii').strip().split('\n')[:-2]

def data_for_css(output):
    try:
        return [ ('%s: %s @line:%d @col:%d') %
            (err['type'],err['message'],err['line'],err['col']) 
            for err in json.loads(output)['messages'] ]

    except:        
        pass
    return []

def data_for_ruby(output):
    try:
        return [ ('%s: %s @line:%d @col:%d') %
                (err['level'], err['message'], err['line'], err['column'])
                for err in json.loads(output) ]
    except:
        pass
    return []

def data_for_cpp(output):     
    return [ err for err in output.decode('ascii').strip().split('\n') \
        if err != '' ]