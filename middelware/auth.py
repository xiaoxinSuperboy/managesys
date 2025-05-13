from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect, render


class LoginMiddleware(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):
        # 0.排除不需要登录就能访问的页面
        # request.path_info  获取当前访问的url
        if request.path_info in ['/user/users/login/', '/user/users/add/', '/user/image/code/']:
            return
        # 1.读取当前访问的用户的session，如果能读到则该用户已经登录过，继续往下执行
        info_dict = request.session.get('info')
        # print(info_dict)
        if info_dict:
            return
        # 2.没有登录过,重新回到登录页面
        return redirect('/user/users/login/')
        # 如果request没有返回值，即为返回none，此时继续向下执行
        # 如果有返回值, HttpResponse, render, redirect ,不在往下执行
        # return HttpResponse('无权访问')

