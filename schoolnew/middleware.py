# from django.contrib.sessions.middleware import SessionMiddleware
# from django.conf import settings

# class NewSessionMiddleware(SessionMiddleware):

#     def process_response(self, request, response):
#         response = super(NewSessionMiddleware, self).process_response(request, response)
#         #You have access to request.user in this method
#         if not request.user.is_authenticated():
#             del response.cookies[]
#         return response
# from django.http import HttpResponse


# class NoCacheMiddleware(object):

#     def process_response(self, request, response):

#         response['Pragma'] = 'no-cache'
#         response['Cache-Control'] = 'no-cache must-revalidate proxy-revalidate'

#         return response
# import re
 
# def _add_to_header(response, key, value):
#     if response.has_header(key):
#         values = re.split(r'\s*,\s*', response[key])
#         if not value in values:
#             response[key] = ', '.join(values + [value])
#     else:
#         response[key] = value
 
# def _nocache_if_auth(request, response):
#     if request.user.is_authenticated():
#         _add_to_header(response, 'Cache-Control', 'no-store')
#         _add_to_header(response, 'Cache-Control', 'no-cache')
#         _add_to_header(response, 'Pragma', 'no-cache')
#     return response
 
# class NoCacheIfAuthenticatedMiddleware(object):
# 	def process_response(self, request, response):
# 		try:
# 			print 'noc 1'
# 			return _nocache_if_auth(request, response)
# 		except:
# 			print 'noc 2'
# 			return response
# 		print 'noc 3'   
# from django.core.cache import caches
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import never_cache
# from django.views.decorators.cache import cache_control

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import never_cache

# class NoCache(object):
#     def process_response(self, request, response):
#         """
#         set the "Cache-Control" header to "must-revalidate, no-cache"
#         """
#         print ' middle-1'
#         if request.path.startswith('/static/'):
#             response['Cache-Control'] = 'must-revalidate, no-cache'
#             print ' middle-2'
#         return response

# def add_never_cache_headers(response):
#     """
#     Adds headers to a response to indicate that a page should never be cached.
#     """
#     patch_response_headers(response, cache_timeout=-1)
#     patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)


# class NeverCacheMixin(object):
# 	@method_decorator(never_cache)
# 	def dispatch(self, *args, **kwargs):
# 		print "Middleware executed"
# 		return super(NeverCacheMixin, self).dispatch(*args, **kwargs)

# class BookMiddleware(object):
# 	def never_cache(view_func):
# 		print "Middleware executed - first"
# 		@wraps(view_func, assigned=available_attrs(view_func))
# 		def _wrapped_view_func(request, *args, **kwargs):
# 			response = view_func(request, *args, **kwargs)
# 			add_never_cache_headers(response)
# 			print "Middleware executed"
# 			return response
# 		print "Middleware executed"
# 		return _wrapped_view_func	
    # def process_request(self, response):
    #     add_never_cache_headers(response)
    #     print "Middleware executed"        
    #     return response  

# original function
 # class BookMiddleware(object):
#     def process_request(self, request):
#         print "Middleware executed"

# class DisableClientSideCachingMiddleware(object):
#     def process_response(self, request, response):


# tried
# class BookMiddleware(object):
# 	def never_cache(view_func):
# 		print "Middleware executed - first"
# 		@wraps(view_func, assigned=available_attrs(view_func))
# 		def _wrapped_view_func(request, *args, **kwargs):
# 			response = view_func(request, *args, **kwargs)
# 			add_never_cache_headers(response)
# 			print "Middleware executed"
# 			return response
# 		print "Middleware executed"
# 		return _wrapped_view_func	