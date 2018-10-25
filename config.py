import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'you-will-never-guess'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_TRACKABLE = True
    SECURITY_RECOVERABLE = False
    SECURITY_PASSWORDLESS = False
    SECURITY_CHANGEABLE = True
    SITE_NAME = "ops-system"
    BOOTSTRAP_SERVE_LOCAL = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    USER_TYPE = ["admin", "dev", "qa", "ops", "dba", "user", "manager"]
    ENVIRONMENT = ["PRD", "DEV", "QA", "STG"]
    SERVER_TYPE = ["server", "other"]
    SERVER_STATUS = ["running", "stopped", "terminated"]
    SLA = ["99999", "9999", "999"]

    ZONE = ["ap-northeast-1a", "ap-northeast-1c", "香港可用区C", "华东 1 可用区 G", "office"]
    REGION = ["hangzhou", "tokyo", "hongkong", "shanghai"]

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    OPS_USER_PER_PAGE = 10
    OPS_server_PER_PAGE = 10

