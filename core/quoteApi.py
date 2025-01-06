# /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
from typing import Union, List
from utils.dt_utilty import market_utc
from core.event import ReqEvent, Meta
from core.async_client import AsyncDatagramClient


class QuoteApi(object):
    """
        udp client 
    """
    def __init__(self, addr):
        # provider_uri
        self.quote_client = AsyncDatagramClient(addr=addr)

    def _on_async(self, req: ReqEvent):
        return self.quote_client.run(req)

    def onSubCalendar(self, s_date:int , e_date: int):
        meta={"start_date": int(s_date), "end_date": int(e_date)}
        req = ReqEvent(rpc_type="calendar", meta=Meta(**meta))
        calendars = self._on_async(req)
        return calendars
    
    def onSubAsset(self, s_date:int , e_date: int, sids: List[str]=[]):
        meta = {"start_date": int(s_date), "end_date": int(e_date), "sid": sids}
        req = ReqEvent(rpc_type="instrument", meta=Meta(**meta))
        instruments = self._on_async(req)
        return instruments

    def onSubIntrady(self, dt: int, sids: List[str]=[]):
        """
            tick data
        """
        s, e = market_utc(dt)
        meta = {"start_date": int(s.timestamp()), "end_date": int(e.timestamp()), "sid": sids}
        req = ReqEvent(rpc_type="dataset", meta=Meta(**meta))
        ticks = self._on_async(req)
        return ticks
    
    def onSubTicks(self, s_date: Union[int, datetime, pd.Timestamp], 
                   e_date: Union[int, datetime, pd.Timestamp], 
                   sids: List[str]=[]):
        """
            tick data
        """
        start_date = s_date.timestamp() if isinstance(s_date, (pd.Timestamp, datetime)) else s_date
        end_date = e_date.timestamp() if isinstance(e_date, (pd.Timestamp, datetime)) else e_date
        meta = {"start_date": int(start_date), "end_date": int(end_date), "sid": sids}
        req = ReqEvent(rpc_type="tick", meta=Meta(**meta))
        ticks = self._on_async(req)
        return ticks
    
    def onSubEvent(self, event_type: str, s_date: int, e_date: int, sids: List[str]=[]):
        """
            adjs / rights
        """
        meta = {"start_date": int(s_date), "end_date": int(e_date), "sid": sids}
        req = ReqEvent(rpc_type=event_type, meta=meta)
        datas = self._on_async(req)
        return datas


