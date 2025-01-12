# /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
from typing import Union, List
from utils.dt_utilty import market_utc
from core.event import QuoteEvent, QuoteMeta
from core.async_client import AsyncDatagramClient


class QuoteApi(object):
    """
        udp client 
    """
    def __init__(self, addr):
        # provider_uri
        self.quote_client = AsyncDatagramClient(addr=addr)

    def _on_async(self, req_meta: QuoteMeta):
        return self.quote_client.run(req_meta)

    def onSubCalendar(self, req_meta: QuoteMeta):
        req = QuoteEvent(rpc_type="calendar", meta=req_meta)
        calendars = self._on_async(req)
        return calendars
    
    def onSubAsset(self, req_meta: QuoteMeta):
        req = QuoteEvent(rpc_type="instrument", meta=req_meta)
        instruments = self._on_async(req)
        return instruments

    def onSubIntrady(self, req_meta: QuoteMeta):
        """
            tick data
        """
        assert req_meta.start_date  == req_meta.end_date, "start_date and end_date must be the same"
        s, e = market_utc(req_meta.start_date)
        meta = {"start_date": int(s.timestamp()), "end_date": int(e.timestamp()), "sid": req_meta.sid}
        req = QuoteEvent(rpc_type="dataset", meta=QuoteMeta(**meta))
        inner_ticks = self._on_async(req)
        return inner_ticks
    
    def onSubTicks(self, req_meta: QuoteMeta):
        """
            tick data
        """
        req = QuoteEvent(event_type="tick", meta=req_meta)
        ticks = self._on_async(req)
        return ticks
    
    def onSubEvent(self, req: QuoteEvent):
        """
            adjs / rights
        """
        datas = self._on_async(req)
        return datas


