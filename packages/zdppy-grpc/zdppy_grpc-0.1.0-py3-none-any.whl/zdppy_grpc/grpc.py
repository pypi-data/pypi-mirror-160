# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  grpc.py
@Time    :  2022/7/23 19:41
@Author  :  张大鹏
@Version :  v0.1.0
@Contact :  lxgzhw@163.com
@License :  (C)Copyright 2022-2023
@Desc    :  描述
"""
# 健康检查
from .health.v1 import health_pb2, health_pb2_grpc
from .health.v1 import health
import grpc


def register_health(server: grpc.Server):
    """
    注册健康检查服务
    """
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
