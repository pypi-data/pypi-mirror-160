from typing import Any, Union

from loguru import logger

from otlpy.base.account import Buy, Cancel, Order, OrderAPI, Replace, Sell
from otlpy.base.market import ORDER_TYPE
from otlpy.base.net import AsyncHttpClient
from otlpy.binance.common import Common


class Spot(OrderAPI):
    def __init__(self, common: Common, client: AsyncHttpClient) -> None:
        super().__init__(has_replace=False)
        self.__common = common
        self.__client = client

    @property
    def _common(self) -> Common:
        return self.__common

    @property
    def _client(self) -> AsyncHttpClient:
        return self.__client

    async def _new_order(self, order: Union[Buy, Sell]) -> None:
        url_path = "/api/v3/order"
        data = self._common.signature(
            {
                "symbol": order.ticker,
                "side": order.oside.name,
                "type": order.otype.name,
                "timeInForce": "GTC",
                "quantity": str(order.qty),
                "price": str(order.price),
            }
        )
        headers = self._common.headers2()
        rheaders, rdata = await self._client.post_params(
            url_path, headers, data
        )
        if not rdata:
            logger.error(
                "\n%s\n%s\n%s\n%s\n%s"
                % (url_path, headers, data, rheaders, rdata)
            )
            return
        order.acknowledgment(rdata, str(rdata["orderId"]), order.qty)

    async def _cancel_order(self, order: Cancel) -> None:
        url_path = "/api/v3/order"
        data = self._common.signature(
            {
                "symbol": order.ticker,
                "orderId": order.origin.rdata["orderId"],
            }
        )
        headers = self._common.headers2()
        rheaders, rdata = await self._client.delete(url_path, headers, data)
        if not rdata:
            logger.error(
                "\n%s\n%s\n%s\n%s\n%s"
                % (url_path, headers, data, rheaders, rdata)
            )
            return
        order.acknowledgment(rdata, "C_" + str(rdata["orderId"]), 0)

    async def buy(
        self, order_type: ORDER_TYPE, ticker: str, qty: float, price: float
    ) -> Buy:
        order = Buy(order_type, ticker, qty, price)
        await self._new_order(order)
        return order

    async def sell(
        self, order_type: ORDER_TYPE, ticker: str, qty: float, price: float
    ) -> Sell:
        order = Sell(order_type, ticker, qty, price)
        await self._new_order(order)
        return order

    async def cancel(self, origin: Order) -> Cancel:
        order = Cancel(origin, ORDER_TYPE.LIMIT)
        await self._cancel_order(order)
        return order

    async def replace(
        self, origin: Order, order_type: ORDER_TYPE, price: float
    ) -> Replace:
        raise NotImplementedError

    async def all_orders(self, ticker: str) -> list[dict[str, Any]]:
        url_path = "/api/v3/allOrders"
        data = self._common.signature(
            {
                "symbol": ticker,
                "startTime": self._common.starttime,
            }
        )
        headers = self._common.headers2()
        rheaders, rdata = await self._client.get(url_path, headers, data)
        if not rdata:
            logger.error(
                "\n%s\n%s\n%s\n%s\n%s"
                % (url_path, headers, data, rheaders, rdata)
            )
            return []
        return list(rdata)

    async def limitorderbook(self, ticker: str) -> dict[str, Any]:
        url_path = "/api/v3/depth"
        data = {
            "symbol": ticker,
        }
        headers = self._common.headers1()
        rheaders, rdata = await self._client.get(url_path, headers, data)
        if not rdata:
            logger.error(
                "\n%s\n%s\n%s\n%s\n%s"
                % (url_path, headers, data, rheaders, rdata)
            )
            return {}
        return dict(rdata)
