"""
Defines config settings based on 'SKELETON_ENV' enviornment variable.
Defaults to development configuration if 'BLOG_ENV' is not set

app_config is used throughout the project to access config settings
for creating the app, using alembic, generating posts, etc.
"""

import os
from settings import DevConfig, ProdConfig, TestConfig

# Config settings
config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}

app_env = os.getenv('SKELETON_ENV')
app_config = config_dict.get(app_env) or DevConfig
