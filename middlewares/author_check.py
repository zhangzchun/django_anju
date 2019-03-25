from django.http import HttpResponse,JsonResponse
from django.utils.deprecation import MiddlewareMixin
class RequestAuth(MiddlewareMixin):
    def process_request(self, request):
        # print(request.GET.get('id'))

        print('请求地址')
        print(request.environ.get('PATH_INFO'))
        # print('111')
        # return HttpResponse('sorry')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        i = 1
        # print('222')
        pass

    def process_exception(self, request, exception):
        print('服务器错误')
        return HttpResponse(exception)

    def process_response(self, request, response):
        # print('444')
        return response
