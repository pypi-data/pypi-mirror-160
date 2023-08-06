# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  model.py
@Time    :  2022/7/24 11:37
@Author  :  张大鹏
@Version :  v0.1.0
@Contact :  lxgzhw@163.com
@License :  (C)Copyright 2022-2023
@Desc    :  描述
"""
from .pool import PooledMySQLDatabase
from .shortcuts import ReconnectMixin
from datetime import datetime
from . import Model, DateTimeField, BooleanField


class MysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    """
    基于连接池和重试机制的MySQL模型
    """
    pass


class SoftDeleteModel(Model):
    """
    软删除基础模型
    """
    # 添加时间
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    # 更新时间
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")
    # 删除时间
    is_deleted = BooleanField(default=False, verbose_name="是否删除")

    def save(self, *args, **kwargs):
        """
        保存方法，自动修改更新时间
        """
        # 判断这是一个新添加的数据还是更新的数据
        if self._pk is not None:
            # 这是一个新数据
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently=False):
        """
        基于类的删除方法
        :param permanently: 是否永久删除
        """
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(self, permanently=False, recursive=False, delete_nullable=False):
        """
        基于对象的删除方法
        :param permanently: 是否永久删除
        :param recursive: 是否递归删除
        :param delete_nullable: 是否删除为null的数据
        :return:
        """
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            self.save()

    @classmethod
    def select(cls, *fields):
        """
        基于类的查询方法，只查找没有被删除的数据
        :param fields: 字段列表
        :return:
        """
        return super().select(*fields).where(cls.is_deleted == False)
