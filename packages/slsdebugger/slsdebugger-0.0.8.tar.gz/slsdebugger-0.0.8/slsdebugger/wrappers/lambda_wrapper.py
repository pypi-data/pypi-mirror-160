import logging
import os
import subprocess
import time
from functools import wraps

from slsdebugger import constants
from slsdebugger.compat import PY2
from slsdebugger.config import config_names
from slsdebugger.config.config_provider import ConfigProvider
from slsdebugger.log.logger import debug_logger
from slsdebugger.timeout import Timeout

logger = logging.getLogger(__name__)


class LambdaWrapper():

    def __init__(self, opts=None):
        self.timeout_margin = ConfigProvider.get(config_names.SLSDEBUGGER_LAMBDA_TIMEOUT_MARGIN,
                                                 constants.DEFAULT_LAMBDA_TIMEOUT_MARGIN)

        self.ptvsd_imported = False
        self.debugger_process = None
        if ConfigProvider.get(config_names.SLSDEBUGGER_ENABLED, 
                    ConfigProvider.get(config_names.SLSDEBUGGER_AUTH_TOKEN)):
            self.initialize_debugger()

    def __call__(self, original_func):
        if hasattr(original_func, "_slsdebugger_wrapped") or \
            not ConfigProvider.get(config_names.SLSDEBUGGER_ENABLED, 
                ConfigProvider.get(config_names.SLSDEBUGGER_AUTH_TOKEN, False)):
            return original_func

        @wraps(original_func)
        def wrapper(event, context):
            if ConfigProvider.get(config_names.SLSDEBUGGER_LAMBDA_WARMUP_WARMUPAWARE,
                                      False) and self.check_and_handle_warmup_request(event):
                    return None

            timeout_duration = self.get_timeout_duration(context)

            # Invoke user handler
            try:
                response = None
                with Timeout(timeout_duration, self.timeout_handler):
                    if ConfigProvider.get(config_names.SLSDEBUGGER_ENABLED, 
                    ConfigProvider.get(config_names.SLSDEBUGGER_AUTH_TOKEN, False)) and self.ptvsd_imported:
                        self.start_debugger_tracing(context)

                    response = original_func(event, context)
            except Exception as e:
                logger.error("Error during to start debugger of Serverless Debugger: {}".format(e))
                raise e
            finally:
                if ConfigProvider.get(config_names.SLSDEBUGGER_ENABLED, 
                ConfigProvider.get(config_names.SLSDEBUGGER_AUTH_TOKEN, False)) and self.ptvsd_imported:
                    self.stop_debugger_tracing()

            return response

        setattr(wrapper, '_slsdebugger_wrapped', True)
        return wrapper

    call = __call__

    def initialize_debugger(self):
        if PY2:
            logger.error("Online debugging not supported in python2.7. Least Supported version is 3.6!")
            return
        try:
            import ptvsd
            self.ptvsd_imported = True
        except Exception as e:
            logger.error("Could not import ptvsd. Thundra ptvsd layer must be added")

    def start_debugger_tracing(self, context):
        try:
            import ptvsd
            ptvsd.tracing(True)

            ptvsd.enable_attach(address=("localhost", ConfigProvider.get(config_names.SLSDEBUGGER_PORT)))
            if not self.debugger_process:
                env = os.environ.copy()
                env['BROKER_HOST'] = str(ConfigProvider.get(config_names.SLSDEBUGGER_BROKER_HOST))
                env['BROKER_PORT'] = str(ConfigProvider.get(config_names.SLSDEBUGGER_BROKER_PORT))
                env['DEBUGGER_PORT'] = str(ConfigProvider.get(config_names.SLSDEBUGGER_PORT))
                env['AUTH_TOKEN'] = str(ConfigProvider.get(config_names.SLSDEBUGGER_AUTH_TOKEN))
                env['SESSION_NAME'] = str(ConfigProvider.get(config_names.SLSDEBUGGER_SESSION_NAME))

                if hasattr(context, 'get_remaining_time_in_millis'):
                    env['SESSION_TIMEOUT'] = str(context.get_remaining_time_in_millis() + int(time.time() * 1000.0))

                debug_bridge_file_path = os.path.join(os.path.dirname(__file__), '../debug/bridge.py')
                self.debugger_process = subprocess.Popen(["python", debug_bridge_file_path], stdout=subprocess.PIPE,
                                                         stdin=subprocess.PIPE, env=env)

            start_time = time.time()
            debug_process_running = True
            while time.time() < (start_time + ConfigProvider.get(config_names.SLSDEBUGGER_WAIT_MAX) / 1000) \
                    and not ptvsd.is_attached():
                if self.debugger_process.poll() is None:
                    ptvsd.wait_for_attach(0.01)
                else:
                    debug_process_running = False
                    break

            if not ptvsd.is_attached():
                if debug_process_running:
                    logger.error('Couldn\'t complete debugger handshake in {} milliseconds.' \
                                 .format(ConfigProvider.get(config_names.SLSDEBUGGER_WAIT_MAX)))
                ptvsd.tracing(False)
            else:
                ptvsd.tracing(True)

        except Exception as e:
            logger.error("error while setting tracing true to debugger using ptvsd: {}".format(e))

    def stop_debugger_tracing(self):
        try:
            import ptvsd
            ptvsd.tracing(False)
            from ptvsd.attach_server import debugger_attached
            debugger_attached.clear()
        except Exception as e:
            logger.error("error while setting tracing false to debugger using ptvsd: {}".format(e))

        try:
            if self.debugger_process:
                o, e = self.debugger_process.communicate(b"fin\n")
                debug_logger("Serverless Debugger process output: {}".format(o.decode("utf-8")))
                self.debugger_process = None
        except Exception as e:
            self.debugger_process = None
            logger.error("error while killing proxy process for debug: {}".format(e))

    def check_and_handle_warmup_request(self, event):

        # Check whether it is empty request which is used as default warmup request
        if not event:
            print("Received warmup request as empty message. " +
                  "Handling with 90 milliseconds delay ...")
            time.sleep(0.1)
            return True
        else:
            if isinstance(event, str):
                # Check whether it is warmup request
                if event.startswith('#warmup'):
                    delayTime = 90
                    args = event[len('#warmup'):].strip().split()
                    # Warmup messages are in '#warmup wait=<waitTime>' format
                    # Iterate over all warmup arguments
                    for arg in args:
                        argParts = arg.split('=')
                        # Check whether argument is in key=value format
                        if len(argParts) == 2:
                            argName = argParts[0]
                            argValue = argParts[1]
                            # Check whether argument is "wait" argument
                            # which specifies extra wait time before returning from request
                            if argName == 'wait':
                                waitTime = int(argValue)
                                delayTime += waitTime
                    print("Received warmup request as warmup message. " +
                          "Handling with " + str(delayTime) + " milliseconds delay ...")
                    time.sleep(delayTime / 1000)
                    return True
            return False

    def get_timeout_duration(self, context):
        timeout_duration = 0
        if hasattr(context, 'get_remaining_time_in_millis'):
            timeout_duration = context.get_remaining_time_in_millis() - self.timeout_margin
            if timeout_duration <= 0:
                timeout_duration = context.get_remaining_time_in_millis() - \
                                   constants.DEFAULT_LAMBDA_TIMEOUT_MARGIN
                logger.warning('Given timeout margin is bigger than lambda timeout duration and '
                               'since the difference is negative, it is set to default value (' +
                               str(constants.DEFAULT_LAMBDA_TIMEOUT_MARGIN) + ')')

        return timeout_duration / 1000.0

    def timeout_handler(self):
        logger.error("<ServerlessDebugger> Task Timeout")