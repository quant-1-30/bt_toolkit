# /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import atexit
import signal
import datetime
import signal
from utils.dt_utilty import market_utc, date2utc
from core.event import Event, ReqEvent
from core.async_client import AsyncDatagramClient


class QuoteApi(object):
    """
        udp client 
    """
    def __init__(self, addr):
        # provider_uri
        self.quote_client = AsyncDatagramClient(addr=addr)
        # validate and ssl

    async def onSubCalendar(self, req_event=None):
        end_date = datetime.datetime.now().strftime("%Y%m%d")
        meta={"start_date": 19900101, "end_date": int(end_date)}
        req = ReqEvent(rpc_type="calendar", meta=meta)
        calendars = self.quote_client.run(req)
        # event
        event = Event(event_type="calendar", data=calendars)
        return event
    
    async def onSubAsset(self, req_event=None):
        # validate args
        s_date = s_date if s_date else 19900101
        e_date = e_date if e_date else datetime.datetime.now().strftime("%Y%m%d")
        meta = {"start_date": int(s_date), "end_date": int(e_date), "sid": sid}
        req = ReqEvent(rpc_type="instrument", meta=meta)
        intruments = self.quote_client.run(req)
        # event
        event = Event(event_type="asset", data=intruments)
        return event

    async def onSubTicks(self, req_event):
        """
            tick data
        """
        s, e = market_utc(date)
        meta = {"start_date": int(s.timestamp()), "end_date": int(e.timestamp()), "sid": sid}
        req = ReqEvent(rpc_type="dataset", meta=meta)
        ticks = self.quote_client.run(req)
        # event
        event = Event(event_type="tick", data=ticks)
        return event

    async def onSubEvent(self, req_event):
        """
            adjs / rights
        """
        meta = {"start_date": int(s_date), "end_date": int(e_date), "sid": sid}
        req = ReqEvent(rpc_type=event_type, meta=meta)
        datas = self.quote_client.run(req)
        # event
        event = Event(event_type="event", data=datas)
        return event


def on_exit(signum, frame):
    print("ctrl + c handler and value", signal.SIGINT.value)
    sys.exit(0)


# ctrl + c
signal.signal(signal.SIGINT, on_exit)

# # set alarm
# signal.signal(signal.alarm, handler)
# signal.alarm(5)



