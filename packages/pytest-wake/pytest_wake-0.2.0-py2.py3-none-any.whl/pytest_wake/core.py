#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   wake.py
@Time    :   2022/07/19 15:37:18
@Version :   1.0
@Desc    :   
"""
import os

import pytest


def pytest_load_initial_conftests(early_config, args, parser):
    for i in args:
        if "--env" in i:
            _, env = i.split("=")
            os.environ["_PYTEST_ENV"] = env
        elif "--tailnum" in i:
            _, tailnum = i.split("=")
            os.environ["_PYTEST_TAILNUM"] = tailnum


@pytest.fixture(scope="session", autouse=True)
def clear_env():
    yield
    if "_PYTEST_TAILNUM" in os.environ:
        del os.environ["_PYTEST_TAILNUM"]
