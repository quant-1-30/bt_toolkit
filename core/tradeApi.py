# /usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List
from core.event import ReqEvent, BrokerEvent, Event, SyncEvent, LogEvent
from core.async_client import AsyncStreamClient


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

    def __init__(self, usr, pwd, auto=True, addr="localhost:8000"):
        # validate and ssl
        self.async_client = AsyncStreamClient(addr)
        self.trade_username = usr
        self.trade_password = pwd
        if auto:
            token = self.on_login(usr, pwd)
        self.trade_token = ""

    # def _emit_event(self, table, meta):
    #     req = ReqEvent(rpc_type=table, meta=meta)
    #     resp = self.async_client.run(req)
    #     return resp[0]

    async def on_login(self, user_id, exp_id):
        pass

    async def on_trade(self, trade_event) -> None:
        pass
    
    async def on_record(self, sync_event) -> None:
        """
            sync close and dividend or right
        """
        pass
    
    async def on_diconnect(self):
        """
            stop tradeApi
        """
