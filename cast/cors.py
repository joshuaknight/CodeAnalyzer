
from django.utils.deprecation import MiddlewareMixin

from cast.settings import ALLOWED_HOSTS, ALLOWED_ORIGIN

class CorsViewMiddleware(MiddlewareMixin):
    """
    Setting the below HTTP headers,
        Access-Control-Allow-Origin
    """

    def __call__(self, request):
        """Handle new-style middleware here."""
        response = self.process_request(request)
        if response is None:
            # If process_request returned None, we must call the next middleware or
            # the view. Note that here, we are sure that self.get_response is not
            # None because this method is executed only in new-style middlewares.
            response = self.get_response(request)

        response = self.process_response(request, response)
        return response
    
    def process_request(self, request):        
        pass

    def process_response(self, request, response):                    
        response['Access-Control-Allow-Origin'] = ALLOWED_ORIGIN
        response['Access-Control-Allow-Methods'] = 'GET ,POST ,PATCH, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = '*'        
        return response