#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class Endpoint(Enum):
    LOGIN = "login"
    TRADE = "trade"
    METRICS = "metrics"


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    WS = "WS"


class QuoteType(Enum):
    DEFAULT = ""
    INSTRUMENT = "instrument"
    CALENDAR = "calendar"
    DATASET = "dataset"
    TICK = "tick"
    ADJUSTMENT = "adjustment"
    RIGHT = "rightment"


class TradeType(Enum):
    LOGIN = "on_login"
    REGISTER = "on_register"
    DEPLOY = "on_deploy"
    TRADE = "on_trade"
    SYNC = "on_sync"
    EVENT = "on_event"
