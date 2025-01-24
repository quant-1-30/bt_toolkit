# /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Any
from urllib.parse import urljoin
from core.meta import LoginMeta, QuoteMeta, OrderMeta, AuthMeta, EventMeta, RangeMeta
from core.async_client import AsyncApiClient
from core.const import ApiEndpoint, ApiMethod
from core.quoteApi import quote_api
from utils.dt_utilty import market_utc
from utils.wrapper import singleton


@singleton
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
    __slots__ = ["async_client", "addr"]

    def __init__(self, addr="http://localhost:8100"):
        # validate and ssl
        self.async_client = AsyncApiClient(addr)
        self.addr = addr

    def on_login(self, login_meta: LoginMeta):
        req = {"endpoint": urljoin(self.addr, ApiEndpoint.LOGIN.value), 
               "method": ApiMethod.POST.value, 
               "params": login_meta.model_dump()}
        resp =self.async_client.run(req)
        return resp
        
    def on_deploy(self, auth_meta: AuthMeta):
        req = {"endpoint": urljoin(self.addr, ApiEndpoint.DEPLOY.value), 
               "method": ApiMethod.GET.value, 
               "params": {"token": auth_meta.token}}
        resp = self.async_client.run(req)
        return resp 
    
    def on_display(self, auth_meta: AuthMeta):
        req = {"endpoint": urljoin(self.addr, ApiEndpoint.DISPLAY.value), 
               "method": ApiMethod.GET.value, 
               "params": {"token": auth_meta.token}}
        resp = self.async_client.run(req)
        return resp 

    def on_trade(self, auth_meta: AuthMeta, order: OrderMeta):

        order_meta = order.model_dump()
        sid = order_meta.pop("sid")
        # build order_meta
        resp = quote_api.onSubAsset(QuoteMeta(sid=[sid]))
        asset_meta = resp[0][0]
        asset_meta.pop("name")

        order_meta["asset"] = asset_meta

        # intraday tickes
        intraday_ticks = quote_api.onSubTicks(QuoteMeta(sid=[sid], 
                                                       start_date=int(order.created_at),
                                                       end_date=int(order.created_at)), 
                                                       intraday=True)

        # params = {"auth": auth_meta.model_dump(),
        params = {
            "experiment_id": auth_meta.experiment_id,
            "orderMeta": order_meta, 
            "meta": intraday_ticks
        }

        # transaction status
        req = {"endpoint": urljoin(self.addr, ApiEndpoint.TRADE.value), 
               "method": ApiMethod.POST.value, 
               "headers": {"Authorization": "Bearer a8894326-edf0-48ff-8a15-ca82e2d8a74f"},
               "params": params}
        resp = self.async_client.run(req)
        return resp
    
    def on_event(self, auth_meta: AuthMeta, event_meta: EventMeta):

        event_data = quote_api.onSubEvent(event_meta.event_type, event_meta.meta)
        params = {
            "experiment_id": auth_meta.experiment_id,
            "meta": event_data,
            "event_type": event_meta.event_type
        }

        req = {"endpoint": urljoin(self.addr, ApiEndpoint.EVENT.value), 
               "method": ApiMethod.POST.value, 
               "headers": {"Authorization": "Bearer a8894326-edf0-48ff-8a15-ca82e2d8a74f"},
               "params": params}
        resp = self.async_client.run(req)
        return resp
    
    def on_sync(self, auth_meta: AuthMeta, meta: QuoteMeta):
        ts = market_utc(meta.start_date, fmt="%Y%m%d")
        resp = quote_api.onSubTicks(QuoteMeta(sid=meta.sid, start_date=ts[1], end_date=ts[1]))
        closes = {item["line"][0][0]: item["line"][0][4] for item in resp}

        params = {
            "experiment_id": auth_meta.experiment_id,
            "meta": closes,
            "session_ix": meta.start_date
        }

        req = {"endpoint": urljoin(self.addr, ApiEndpoint.SYNC.value), 
               "method": ApiMethod.POST.value, 
               "headers": {"Authorization": "Bearer a8894326-edf0-48ff-8a15-ca82e2d8a74f"},
               "params": params}
        resp = self.async_client.run(req)
        return resp
    
    def on_account(self, auth_meta: AuthMeta, meta: RangeMeta) -> Dict[str, Any]:
        """
            sync close and dividend or right
        """
        params = {
            "experiment_id": auth_meta.experiment_id,
            "meta": meta.model_dump()
        }
        req = {"endpoint": urljoin(self.addr, ApiEndpoint.ACCOUNT.value), 
               "method": ApiMethod.GET.value,
               "headers": {"Authorization": "Bearer a8894326-edf0-48ff-8a15-ca82e2d8a74f"},
               "params": params}
        resp = self.async_client.run(req)
        return resp
    
    def on_metrics(self, auth_meta: AuthMeta, meta: QuoteMeta) -> Dict[str, Any]:
        """
            sync close and dividend or right
        """
        params = {
            "experiment_id": auth_meta.experiment_id,
            "meta": meta.model_dump()
        }
        req = {"endpoint": urljoin(self.addr, ApiEndpoint.METRICS.value), 
               "method": ApiMethod.GET.value, 
               "headers": {"Authorization": "Bearer a8894326-edf0-48ff-8a15-ca82e2d8a74f"},
               "params": params}
        metrics = self.async_client.run(req)
        return metrics
