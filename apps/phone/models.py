from django.db import models


# Create your models here.
class Phone(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)
    level_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)
    status_choices = (
        (1, '未占用'),
        (2, '已占用'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)
