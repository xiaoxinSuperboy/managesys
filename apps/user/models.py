from django.db import models


# from apps.web.models import Department


# Create your models here.
class Employee(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='员工姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')
    # 级联删除  on_delete = models.CASCADE  ，，或离职就为空，滞空
    depart = models.ForeignKey(verbose_name='部门', to='web.Department', to_field='id', on_delete=models.CASCADE)  # 外键
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
