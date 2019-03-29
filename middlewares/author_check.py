from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from utils.my_token import *


class RequestAuth(MiddlewareMixin):
    def process_request(self, request):
        # print(request.GET.get('id'))

        print('请求地址')
        print(request.environ.get('PATH_INFO'))
        url = request.environ.get('PATH_INFO')

        # 需要验证token的路由
        url_check = ['/collect/increaseCollection/',
                     '/collect/cancelCollection/',
                     '/collect/checkCollection/',
                     '/comment/addComment/',
                     '/comment/addReply/',
                     '/user/addAppointment/']

        if url in url_check:
            res = checkToken(request.headers.get('token'))
            if not res:
                return JsonResponse({"status_code": "10006", "status_text": "登录过期"})

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
