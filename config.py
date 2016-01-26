import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOCHAT_MAIL_SUBJECT_PREFIX = '[Lochat]'
    LOCHAT_MAIL_SENDER = 'Lochat Admin <admin@lochat.com>'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_SETTINGS = {'db': os.environ.get('DEV_DATABASE_URL') or
                      'dev_lochat_db'}


class TestingConfig(Config):
    TESTING = True
    MONGO_SETTINGS = {'db': os.environ.get('TEST_DATABASE_URL') or
                      'test_lochat_db'}


class ProductionConfig(Config):
    MONGO_SETTINGS = {'db': os.environ.get('DATABASE_URL')}


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
}


