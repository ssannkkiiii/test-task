from django.http import JsonResponse
from django.conf import settings

class APIVersionMiddleware:
   
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_version = request.META.get('HTTP_X_API_VERSION')
        
        if not api_version:
            path_parts = request.path.split('/')
            if len(path_parts) >= 3 and path_parts[1] == 'api':
                version = path_parts[2]
                if version in settings.SUPPORTED_API_VERSIONS:
                    api_version = version
        
        if not api_version:
            api_version = settings.DEFAULT_API_VERSION
        
        if api_version not in settings.SUPPORTED_API_VERSIONS:
            return JsonResponse({
                'error': f'Unsupported API version: {api_version}',
                'supported_versions': settings.SUPPORTED_API_VERSIONS
            }, status=400)
        
        request.api_version = api_version
        
        response = self.get_response(request)
        return response
