from __future__ import absolute_import

from importlib import import_module as _import_module

from slsdebugger.config import config_names
from slsdebugger.config.config_provider import ConfigProvider

from slsdebugger.wrappers.wrapper_factory import WrapperFactory as _WrapperFactory

import logging
logger = logging.getLogger(__name__)

if not ConfigProvider.get(config_names.SLSDEBUGGER_AUTH_TOKEN, False):
    logger.info("Please enter valid value for SLSDEBUGGER_AUTH_TOKEN!!!")

def lambda_wrapper(func):
    from slsdebugger.wrappers.lambda_wrapper import LambdaWrapper
    return _WrapperFactory.get_or_create(LambdaWrapper)(func)


__all__ = [
    'lambda_wrapper'
]
