from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from apps.phone import models
from django import forms


# Create your views here.


def num_list(request):
    # 拿到数据库的所有靓号
    # data = models.Phone.objects.all().order_by('-level')  # 按级别倒序
    # for i in range(300):
    #     models.Phone.objects.create(mobile='18888888', price='200', level='2', status='1')
    # 搜索
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['mobile__contains'] = search_data

    # 根据用户需要访问的页码计算起始位置
    page = int(request.GET.get('page', 1))
    next_page = page + 1
    ago_page = page - 1
    start = (page - 1) * 10
    end = page * 10
    data = models.Phone.objects.filter(**data_dict)[start:end]
    return render(request, 'phone/numlist.html', {'data': data, 'search_data': search_data, 'next_page': next_page, 'ago_page': ago_page})


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# 创建一个ModelForm继承类
class PhoneForm(forms.ModelForm):
    # 验证方式一 ,需要导入from django.core.validators import RegexValidator

    # mobile = forms.CharField(
    #     label='手机号',
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    # )

    class Meta:
        # 指定模型类
        model = models.Phone
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    # 方式二  需要导入from django.core.exceptions import ValidationError
    def clean_mobile(self):
        # 拿到该数据,手机号
        data = self.cleaned_data['mobile']
        exists = models.Phone.objects.filter(mobile=data).exists()
        if exists:
            raise ValidationError('手机号已存在')
        # if len(data) != 11:
        #     raise ValidationError('格式错误')
        return data


def num_add(request):
    if request.method == 'GET':
        # 实例化对象
        form = PhoneForm()
        return render(request, 'phone/numadd.html', {'form': form})
    # 若为post
    # 拿到用户输入数据
    form = PhoneForm(data=request.POST)
    # 数据验证
    if form.is_valid():
        form.save()
        return redirect('/phone/numlist/')
    return render(request, 'phone/numadd.html', {'form': form})


class PhoneeditForm(forms.ModelForm):
    mobile = forms.CharField(disabled=True, label='手机号')

    class Meta:
        # 指定模型类
        model = models.Phone
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}


def edit_num(request, nid):
    # 通过nid获取当前的元素
    cur_obj = models.Phone.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PhoneeditForm(instance=cur_obj)
        return render(request, 'phone/numedit.html', {'form': form})
    # 若为post请求
    # 拿到用户输入数据
    form = PhoneeditForm(data=request.POST, instance=cur_obj)
    if form.is_valid():
        form.save()
        return redirect('/phone/numlist/')
    return redirect(request, 'phone/numedit.html', {'form': form})


def delete_num(request, nid):
    # 获取当前元素
    models.Phone.objects.filter(id=nid).delete()
    return redirect('/phone/numlist/')
