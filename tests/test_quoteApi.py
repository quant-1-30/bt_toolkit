import pytest
import numpy as np
import datetime
from core.quoteApi import QuoteApi
from core.event import ReqEvent, Meta

# reuse / dependency / setup / teardown

class TestQuoteApi:
    
    @pytest.fixture
    def quote_api(self):
        return QuoteApi(addr=("127.0.0.1",9999))
    
    @pytest.fixture
    def req_event(self):
        # return ReqEvent(rpc_type="calendar", meta=Meta(start_date=19900101))
        return 19900101, 30000202
    
    @pytest.fixture
    def req_tick_event(self):
        return 1728351060, 1728351600, ["603676"]
    
    # def test_onSubCalendar(self, quote_api, req_event):
    #     data = quote_api.onSubCalendar(*req_event)
    #     # print(data)

    # def test_onSubAsset(self, quote_api, req_event):
    #     data = quote_api.onSubAsset(*req_event)
    #     print(data)

    # def test_onSubTicks(self, quote_api, req_tick_event):
    #     data = quote_api.onSubTicks(*req_tick_event)
    #     print(data)

    def test_onSubEvent(self, quote_api, req_event):
        quote_api.onSubEvent("tick", *req_event)



