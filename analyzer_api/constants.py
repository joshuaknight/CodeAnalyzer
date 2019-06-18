
from analyzer_api import _process

available_lang = [
    'python',
    'c',
    'cpp',    
    'ruby',
    'html',
    'css',
    'javascript'    
]

get_arg_for_language = {
    'python' : 'mypy %r --show-column-numbers',
    'javascript' : 'jshint %r',
    'html' : 'htmlhint %r -f json',
    'css' : 'csslint %r --format=json',
    'ruby' : 'ruby-lint %r --presenter json',
    'c' : 'cppcheck -q --enable=warning,performance,unusedFunction,style error --inconclusive --std=posix %r',
    'cpp' : 'cppcheck -q --enable=warning,performance,unusedFunction,style error --inconclusive --std=posix %r'
}

get_exec_for_language = {
    'python' : 'py',
    'html' : 'html',    
    'css' :'css',
    'javascript' : 'js',
    'ruby' : 'rb',
    'c' : 'c',
    'cpp' : 'cpp'
}

get_func_for_lang = {
    'python' : _process.data_for_python,
    'html' : _process.data_for_html,
    'css' : _process.data_for_css,
    'javascript' : _process.data_for_javascript,
    'ruby' : _process.data_for_ruby,
    'c' : _process.data_for_cpp,
    'cpp' : _process.data_for_cpp
}