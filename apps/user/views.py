from django.shortcuts import render, redirect, HttpResponse
from apps.user import models
from apps.web.models import Department
from django import forms


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


def user_login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    # 认为post请求
    # 拿到用户登录的数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 拿到数据库所有用户信息
    userslist = models.Employee.objects.all()
    print(username)
    print(password)
    for item in userslist:
        if item.name == username and item.password == password:
            return render(request, 'user/login_successful.html')
    else:
        return HttpResponse('用户名或密码错误')


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
