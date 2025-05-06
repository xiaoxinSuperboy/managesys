from django.shortcuts import render, redirect
from apps.web import models


# Create your views here.
def depart_list(request):
    """显示部门列表"""
    departList = models.Department.objects.all()
    return render(request, 'web/depart_list.html', {'departList': departList})


def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, 'web/depart_add.html')
    # 获取用户的提交的数据
    name = request.POST.get('depart_name')
    # 保存数据到数据库
    models.Department.objects.create(title=name)
    # 重定向
    return redirect('/web/depart/list/')


def depart_delete(request):
    """删除部门"""
    # 获取数据
    nid = request.GET.get('nid')
    # 删除数据
    models.Department.objects.filter(id=nid).delete()
    return redirect('/web/depart/list/')


def depart_edit(request):
    """修改部门"""
    # 获取未修改的title
    old_title = request.GET.get('title')
    if request.method == 'GET':
        return render(request, 'web/depart_edit.html', {'old_title': old_title})
    # 获取修改后的数据
    name = request.POST.get('depart_name')
    models.Department.objects.filter(title=old_title).update(title=name)
    return redirect('/web/depart/list/')
