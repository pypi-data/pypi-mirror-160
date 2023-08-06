from slsdebugger.config import config_names

CONFIG_METADATA = {
    config_names.SLSDEBUGGER_ENABLED: {
        'type': 'boolean',
        'defaultValue': True
    },
    config_names.SLSDEBUGGER_LAMBDA_HANDLER: {
        'type': 'string',
    },
    config_names.SLSDEBUGGER_LAMBDA_WARMUP_WARMUPAWARE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.SLSDEBUGGER_LAMBDA_TIMEOUT_MARGIN: {
        'type': 'int',
    },
    config_names.SLSDEBUGGER_PORT: {
        'type': 'int',
        'defaultValue': 1111,
    },
    config_names.SLSDEBUGGER_LOGS_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.SLSDEBUGGER_WAIT_MAX: {
        'type': 'int',
        'defaultValue': 60000,
    },
    config_names.SLSDEBUGGER_IO_WAIT: {
        'type': 'int',
        'defaultValue': 2000,
    },
    config_names.SLSDEBUGGER_BROKER_PORT: {
        'type': 'int',
        'defaultValue': 444,
    },
    config_names.SLSDEBUGGER_BROKER_HOST: {
        'type': 'string',
        'defaultValue': 'broker.service.serverlessdebugger.com',
    },
    config_names.SLSDEBUGGER_SESSION_NAME: {
        'type': 'string',
        'defaultValue': 'default',
    },
    config_names.SLSDEBUGGER_AUTH_TOKEN: {
        'type': 'string',
    }
}
