"""
Configuration settings for the Hini App.

The definition of the different configuration settings is contained here:
- Development Configuration
- Testing Configuration
- Production Configuration
"""
import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class BaseConfig:
    """
    The definition of the global configuration is defined here.

    Attributes such as SECRET_KEY are the same no matter the platform used.
    """

    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = None
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    OAUTHLIB_INSECURE_TRANSPORT = '0'


class DevelopmentConfig(BaseConfig):
    """
    The configuration settings for development mode is defined here.

    Attributes such as DEBUG are different for other
    environments, so they are defined in a class called DevelopmentConfig.
    """

    ENV = 'development'
    FLASK_ENV = 'development'
    OAUTHLIB_INSECURE_TRANSPORT = '1'


class ProductionConfig(BaseConfig):
    """
    The configuration settings for production mode is defined here.

    Attributes such as DEBUG are different for other
    environments, so they are defined in a class called ProductionConfig.
    """

    DEBUG = False
    ENV = 'production'
    FLASK_ENV = 'production'


# Object containing the different configuration classes.
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
