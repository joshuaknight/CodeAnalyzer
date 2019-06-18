

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from analyzer_api.models import AvailableLanguages

from analyzer_api.suite import AnalyzeCodeAPI

import json

def available_languages(request):    
    return JsonResponse(AvailableLanguages.to_json(),status = 200)

@csrf_exempt
def analyze_code(request,lang):

    if request.method == 'POST':                                
        
        body = json.loads(request.body)

        analyzer = AnalyzeCodeAPI(lang=lang,data = body.get('data'))        

        return JsonResponse(analyzer.analyze_file(),status = 200)

    if request.method == 'OPTIONS':
        return JsonResponse({},status = 200)

    return JsonResponse({
        'error' : ['Method Not Allowed']
    },status = 405)