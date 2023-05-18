"""
日志 django中间件
"""
from django.utils.deprecation import MiddlewareMixin


class CorsMiddleWare(MiddlewareMixin):
    def process_response(self, request, response):
        if request.META.get("HTTP_REFERER") is not None:
            response["Access-Control-Allow-Methods"] = "*"
            response["Access-Control-Allow-Credentials"] = True
            response['Access-Control-Allow-Headers'] = "Authorization"
            response["Access-Control-Allow-Origin"] = "/".join(request.META.get("HTTP_REFERER").split("/")[0:3])
            return response
        else:
            return response
