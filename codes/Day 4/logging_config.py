import logging
from logging.config import dictConfig
import os
os.makedirs("logs", exist_ok=True)

# Simple logging config 
LOGGING_CONFIG = {
    'version':1,
    'formatters':{
        'default':{
            'format':'[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
    'handlers':{
        'file':{
            'class':'logging.FileHandler',
            'filename':'logs/school_api.log',
            'formatter':'default',
        },
        'console':{
            'class':'logging.StreamHandler',
            'formatter':'default',
        }, 
    },
    'loggers':{
        '':{
            'level':'DEBUG',
            'handlers':['file','console'],
        },
    }
}

# Configure logging once, at app startup
dictConfig(LOGGING_CONFIG)
# Optionally create a module-level logger you can import everywhere
logger = logging.getLogger(__name__)
logger.info('✅ Logging Configured Successfully')



# "loggers": {
#         "auth_hashing": {
#             "handlers": ["console", "file_auth"],
#             "level": "DEBUG",
#             "propagate": False  # <---- Add this here to stop duplication
#         },
#         "": {  # root logger
#             "handlers": ["console"],
#             "level": "WARNING",
#         },
#     },