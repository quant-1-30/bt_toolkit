# /usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict, Any
from core.event import LoginEvent,TradeEvent
from core.async_client import AsyncWebClient
from core.const import Endpoint, Method


class TradeApi(object):
    """
    # How to implement a tradeApi:
    ---
    ## Basics
    A tradeApi should satisfies:
    * this class should be thread-safe:
        * all methods should be thread-safe
        * no mutable shared properties between objects.
    * all methods should be non-blocked
    * satisfies all requirements written in docstring for every method and callbacks.
    * automatically reconnect if connection lost.

    All the XxxData passed to callback should be constant, which means that
        the object should not be modified after passing to on_xxxx.
    So if you use a cache to store reference of data, use copy.copy to create a new object
    before passing that data into on_xxxx
    """
    __slots__ = ("fund",)

    def __init__(self, addr="localhost:8000"):
        # validate and ssl
        self.async_client = AsyncWebClient(addr)
        self.trade_token = ""

    def on_login(self, login_event: LoginEvent):
        # return token   
        req = {"endpoint": Endpoint.LOGIN, "method": Method.POST, "params": login_event.model_dump()}
        resp =self.async_client.run(req)
        if resp["token"]:
            self.trade_token = resp["token"]
            return True
        return False

    def on_trade(self, trade_event: TradeEvent):
        # transaction status
        req = {"endpoint": Endpoint.TRADE, "method": Method.POST, "params": trade_event.model_dump()}
        status = self.async_client.run(req)
        return status
    
    def on_metrics(self, sdate, edate) -> Dict[str, Any]:
        """
            sync close and dividend or right
        """
        req = {"endpoint": Endpoint.METRICS, "method": Method.GET, "params": {"sdate": sdate, "edate": edate}}
        metrics = self.async_client.run(req)
        return metrics
