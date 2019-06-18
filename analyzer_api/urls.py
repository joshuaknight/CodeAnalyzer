

from django.urls import path

from analyzer_api import api

urlpatterns = [
    path( 'available-lang', api.available_languages ),
    path( '<lang>', api.analyze_code )
]