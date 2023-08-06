DATABASE_AUTO_CREATE_INDEX = True
DATABASES = {
    'default': {
        'db': 'billing',
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': ''
    }
}

CACHES = {
    'default': {},
    'local': {
        'backend': 'spaceone.core.cache.local_cache.LocalCache',
        'max_size': 128,
        'ttl': 300
    }
}

LOG = {
    'filters' : {
        'masking' : {
            'rules' : {
                'Billing.get_data': ['secret_data']
            }
        }
    }
}

HANDLERS = {
}

CONNECTORS = {
    'BillingPluginConnector': {
    },
    'SpaceConnector': {
        'backend': 'spaceone.core.connector.space_connector.SpaceConnector',
        'endpoints': {
            'identity': 'grpc://identity:50051',
            'plugin': 'grpc://plugin:50051',
            'repository': 'grpc://repository:50051',
            'secret': 'grpc://secret:50051',
            'config': 'grpc://config:50051',
        }
    },
}

INSTALLED_DATA_SOURCE_PLUGINS = [
    # {
    #     'name': '',
    #     'plugin_info': {
    #         'plugin_id': '',
    #         'version': '',
    #         'options': {},
    #         'secret_data': {},
    #         'schema': '',
    #         'upgrade_mode': ''
    #     },
    #     'tags':{
    #         'description': ''
    #     }
    # }
]
