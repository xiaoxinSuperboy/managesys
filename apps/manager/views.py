from django.shortcuts import render, redirect
from apps.manager import models
from django import forms
from django.core.exceptions import ValidationError
from apps.manager.utils import encrypt


# Create your views here.
def admin_list(request):
    """管理员列表"""
    # 拿到数据库的对象
    data = models.Manager.objects.all()
    context = {
        'data': data
    }
    return render(request, 'manager/admin_list.html', context)


class AdminModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        # 指定模型类
        model = models.Manager
        fields = ['username', 'password', 'confirm_password', ]

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     for name, field in self.fields.items():
        #         field.widget.attrs = {'class': 'form-control'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
            # render_value=True保留不清空
        }

        # clean_data拿到用户输入的所有数据返回一个字典

    # 给密码加密
    def clean_password(self):
        password = self.cleaned_data['password']
        return encrypt.md5(password)

    # 钩子方法
    def clean_confirm_password(self):
        print(self.cleaned_data)
        confirm_password = self.cleaned_data['confirm_password']
        # 此时获取到的password已经加密了
        password = self.cleaned_data['password']
        # 把confirm_password也加密
        confirm = encrypt.md5(confirm_password)
        if confirm != password:
            raise ValidationError('两次输入不一致')
        return confirm


def admin_add(request):
    """添加管理员"""
    form = AdminModelForm()
    if request.method == 'GET':
        return render(request, 'add.html', {'form': form, 'Title': '新建管理员', 'title': '新建管理员'})
    # 若为post请求
    # 拿到用户输入数据
    data = AdminModelForm(data=request.POST)
    if data.is_valid():
        data.save()  # 提交数据
        return redirect('/manager/admin/list/')
    return render(request, 'add.html', {'form': data, 'Title': '新建管理员', 'title': '新建管理员'})


class EditUsername(forms.ModelForm):
    class Meta:
        model = models.Manager
        fields = ['username', ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


def admin_edit(request, nid):
    """编辑管理员"""
    cur_obj = models.Manager.objects.filter(id=nid).first()
    if not cur_obj:
        return redirect('/manager/list/')
    Title = '编辑管理员用户名'
    title = '编辑管理员用户名'
    if request.method == 'GET':
        form = EditUsername(instance=cur_obj)
        return render(request, 'add.html', {'form': form, 'Title': Title, 'title': title})
    # 若为post请求
    data = EditUsername(data=request.POST, instance=cur_obj)  # 拿到数据
    if data.is_valid():
        data.save()
        return redirect('/manager/admin/list/')


def admin_delete(request, nid):
    models.Manager.objects.filter(id=nid).delete()
    return redirect('/manager/admin/list/')
