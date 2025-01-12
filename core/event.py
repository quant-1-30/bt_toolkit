# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:37:47 2019

@author: python
"""
import pydantic
from pydantic import Field, field_validator
from const import QuoteType, TradeType
from typing import List, Union, Tuple, Mapping, Any, Dict


def nop_context():
    pass


class QuoteMeta(pydantic.BaseModel):
    start_date: int = Field(default=19900101)
    end_date: int = Field(default=30000101)
    sid: List[str] = Field(default=[])


class QuoteEvent(pydantic.BaseModel):
    event_type: QuoteType = QuoteType.DEFAULT
    quote_meta: QuoteMeta

    @field_validator(mode="before")
    def validate_event_type(cls, v):
        assert v in [QuoteType.DEFAULT, QuoteType.INSTRUMENT, QuoteType.CALENDAR, QuoteType.DATASET, QuoteType.TICK, QuoteType.ADJUSTMENT, QuoteType.RIGHT], "Invalid event type"
        return v


class LoginMeta(pydantic.BaseModel):
    user_id: str
    account_id: str


class LoginEvent(pydantic.BaseModel):

    event_type: str
    login_meta: LoginMeta

    @field_validator(mode="before")
    def validate_event_type(cls, v):
        assert v in [TradeType.LOGIN, TradeType.REGISTER, TradeType.DEPLOY], "Invalid event type"
        return v

    # _secret: str = "hidden"  # Private attribute
    # model_config = {"private_attributes": {"_secret"}}


class TradeMeta(pydantic.BaseModel):
    
    sid: str
    amount: int  
    volume: int                                                                                                                                       


class TradeEvent(pydantic.BaseModel):
    
    event_type: str
    execution_style: str
    trade_meta: TradeMeta
    token: str

    @field_validator(mode="before")
    def validate_event_type(cls, v):
        assert v in [TradeType.TRADE, TradeType.SYNC, TradeType.EVENT], "Invalid event type"
        return v


class LogEvent(pydantic.BaseModel):

    log_level: str
    log_meta: Any
