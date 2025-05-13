from django.shortcuts import render, redirect, HttpResponse
from apps.user import models
from apps.web.models import Department
from django import forms
from apps.manager.utils import encrypt
from apps.manager import models as manager_models
from apps.user.utils import verifycode


# Create your views here.
def user_list(request):
    """用户管理"""
    # 获取数据库用户信息
    users_list = models.Employee.objects.all()
    return render(request, 'user/user_list.html', {'users_list': users_list})


def user_add(request):
    """用户添加"""
    if request.method == 'GET':
        department = Department.objects.all()
        return render(request, 'user/user_add.html', {'department': department})
    # 若为POST请求
    # 拿到用户提交的数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    createdate = request.POST.get('createdate')
    gender = request.POST.get('gender')
    departname = request.POST.get('departname')
    # 提交给数据库
    models.Employee.objects.create(name=username, password=password, age=age, account=account, create_time=createdate,
                                   gender=gender, depart_id=departname)
    # 返回用户列表页面
    return redirect('/user/users/list/')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        required=True
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-left:15px'}),
        required=True
    )

    def clean_password(self):
        # 拿到password
        pwd = self.cleaned_data.get('password')
        md5_pwd = encrypt.md5(pwd)
        return md5_pwd


def user_login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/user_login.html', {'form': form})
    # 认为post请求
    # 拿到用户登录的数据
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 对验证码进行校验
        # 拿到用户输入的验证码 ,并且删除code防止在数据库查询用户名密码时查询到code
        in_code = form.cleaned_data.pop('code')
        print(in_code)
        # 拿到session中的code
        code = request.session.get('image_code', '')
        print(code)
        # 去与session中的验证码进行比较
        if in_code != code:

            # 验证成功，获取到的用户名和密码
            # print(form.cleaned_data)
            form.add_error('code', '验证码错误')
            return render(request, 'user/user_login.html', {'form': form})
            # 去数据库校验用户名和密码
        cur_obj = manager_models.Manager.objects.filter(**form.cleaned_data).first()
        # 未匹配到对象
        if not cur_obj:
            # 增加一个错误信息
            form.add_error('password', '用户名或密码错误')
            return render(request, 'user/user_login.html', {'form': form})


            # 匹配成功,即用户名和密码正确
            # 网站生成随机字符串，写到用户浏览器的cookie中,在写入到session
        request.session['info'] = {
                    'id': cur_obj.id,
                    'username': cur_obj.username
                }
        request.session.set_expiry(60*60*24*7)
        return redirect('/manager/admin/list/')
    return render(request, 'user/user_login.html', {'form': form})


from io import BytesIO


def image_code(request):
    """图片验证码"""
    # 调用含pillow的函数,生成图片
    img, code_str = verifycode.verify_code()
    print(code_str)
    # 把验证码写入到session中
    request.session['image_code'] = code_str
    # 给session设置60秒超时
    request.session.set_expiry(60)
    # 图片写入内存
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


def user_logout(request):
    """注销"""
    request.session.clear()
    return redirect('/user/users/login/')


# 创建一个类继承modelform
class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.Employee  # 指定模型类
        fields = ['name', 'password', 'age', 'account', 'create_time', 'depart', 'gender']

    # 给modelform里面的标签添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}


def user_addmodel(request):
    # 若为GET请求
    if request.method == 'GET':
        # 实例化对象，拿到数据库用户列表
        form = UserModelForm()
        return render(request, 'user/user_addmodel.html', {'form': form})
    # 若为post请求
    # 用户提交的数据进行验证
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # # 拿到用户输入的数据如果有效
        # name = request.POST.get('name')
        # password = request.POST.get('password')
        # age = request.POST.get('age')
        # account = request.POST.get('account')
        # createtime = request.POST.get('create_time')
        # depart = request.POST.get('depart')
        # gender = request.POST.get('gender')
        # models.Employee.objects.create(name=name, password=password, age=age, account=account, create_time=createtime,
        #                                depart_id=depart, gender=gender)
        form.save()
        return redirect('/user/users/list/')
    else:
        return render(request, 'user/user_addmodel.html', {'form': form})


def user_edit(request):
    """编辑用户"""
    nid = request.GET.get('nid')
    row_obj = models.Employee.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据nid来获取需要编辑的那一行数据
        form = UserModelForm(instance=row_obj)
        return render(request, 'user/user_edit.html', {'form': form})
    # 若为post请求
    # 拿到用户输入数据
    form = UserModelForm(data=request.POST, instance=row_obj)
    # 进行数据校验
    if form.is_valid():
        form.save()
        return redirect('/user/users/list/')


def user_delete(request):
    nid = request.GET.get('nid')
    models.Employee.objects.filter(id=nid).delete()
    return redirect('/user/users/list/')
