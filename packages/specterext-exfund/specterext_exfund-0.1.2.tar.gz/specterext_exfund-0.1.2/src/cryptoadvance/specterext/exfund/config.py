"""
Here Configuration of your Extension (and maybe your Application) takes place
"""
import os
from cryptoadvance.specter.config import ProductionConfig as SpecterProductionConfig


class BaseConfig:
    """This is a extension-based Config which is used as Base"""

    EXFUND_ASSETS_REGISTRY = {
        "liquidv1": "https://assets.blockstream.info/",
        "liquidtestnet": "https://assets-testnet.blockstream.info/"
    }


class ProductionConfig(BaseConfig):
    """This is a extension-based Config for Production"""

    pass

