import pytest
import numpy as np
import datetime
from core.tradeApi import *
from core.meta import LoginMeta, QuoteMeta, OrderMeta, EventMeta

# reuse / dependency / setup / teardown

class TestQuoteApi:

    @pytest.fixture
    def trade_api(self):
        return TradeApi(addr="http://localhost:8100")
    
    @pytest.fixture
    def req_login(self):
        # return ReqEvent(rpc_type="calendar", meta=Meta(start_date=19900101))
        return LoginMeta(name="test", phone=1234567890, email="test@test.com")
    
    @pytest.fixture
    def req_auth(self):
        return AuthMeta(token="70d4c731-484a-402e-9d64-2b83ba6558cc", 
                        experiment_id="22e31ca3-c741-47aa-825d-0adf4b074ef6")
                        # experiment_id="")
    
    @pytest.fixture
    def req_trade(self):
        return OrderMeta(sid="603676", order_type=4, direction=1, created_at="202410081405", price=100, amount=10000000)
    
    @pytest.fixture
    def req_event(self):
        # return EventMeta(event_type="adjustment", meta=QuoteMeta(sid=["603676"]))
        return EventMeta(event_type="rightment", meta=QuoteMeta(sid=["603676"]))
    
    @pytest.fixture
    def req_sync(self):
        return QuoteMeta(sid=["603676"], start_date=20241008, end_date=20241008)
    
    # def test_onLogin(self, trade_api, req_login):
    #     data = trade_api.on_login(req_login)
    #     print(data)
    #     assert data is not None

    # def test_onDeploy(self, trade_api, req_auth):
    #     data = trade_api.on_deploy(req_auth)
    #     print(data)

    # def test_onTrade(self, trade_api, req_auth, req_trade):
    #     data = trade_api.on_trade(req_auth, req_trade)
    #     print(data)

    # def test_onEvent(self, trade_api, req_auth, req_event):
    #     data = trade_api.on_event(req_auth, req_event)
    #     print(data)

    def test_onSync(self, trade_api, req_auth, req_sync):
        data = trade_api.on_sync(req_auth, req_sync)
        print(data)

    # def test_onAccount(self, trade_api, req_auth, req_event):
    #     data = trade_api.on_account(req_auth, req_event)
    #     print(data)

    # def test_onMetrics(self, trade_api, req_auth, req_event):
    #     data = trade_api.on_metrics(req_auth, req_event)
    #     print(data)

