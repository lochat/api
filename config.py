import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOCHAT_MAIL_SUBJECT_PREFIX = '[Lochat]'
    LOCHAT_MAIL_SENDER = 'Lochat Admin <admin@lochat.com>'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = os.environ.get('DEV_DATABASE_URL') or 'dev_lochat_db'


class TestingConfig(Config):
    TESTING = True
    MONGODB_DB = os.environ.get('TEST_DATABASE_URL') or 'test_lochat_db'


class ProductionConfig(Config):
    MONGODB_DB = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
}


