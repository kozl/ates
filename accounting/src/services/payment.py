import logging
from functools import lru_cache

from core.logger import LOGGING


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class DummyPaymentGateway():
    def pay(self, username: str, amount:int ):
        logger.info(f"Payment of {amount}$ to {username} made")


@lru_cache()
def get_payment_gateway():
    return DummyPaymentGateway()