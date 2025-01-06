# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import pydantic
from pydantic import Field
import numpy as np
from enum import Enum
from numpy import isfinite
from dataclasses import dataclass, field
from typing import List, Union, Tuple, Mapping, Any, Dict
from collections import namedtuple


def nop_context():
    pass


class Meta(pydantic.BaseModel):
    start_date: int = Field(default=19900101)
    end_date: int = Field(default=30000101)
    sid: List[str] = Field(default=[])


class ReqEvent(pydantic.BaseModel):

    rpc_type: str
    # meta: Mapping[str, Any] = {}
    meta: Meta = Meta()

    # _secret: str = "hidden"  # Private attribute

    # model_config = {"private_attributes": {"_secret"}}


class LogEvent(pydantic.BaseModel):

    log_level: str
    log_meta: Any

