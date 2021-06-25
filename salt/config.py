import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test2.db'
    # SQLALCHEMY_DATABASE_URI = (
    #     f'postgresql+psycopg2://{os.environ.get("AUDIOGUILD_POSTGRES_USER")}:' +
    #     f'{os.environ.get("AUDIOGUILD_POSTGRES_PW")}@{os.environ.get("AUDIOGUILD_DATABASE_URL")}/{os.environ.get("AUDIOGUILD_DATABASE_DB")}'
    # )
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{os.environ.get("AUDIOGUILD_POSTGRES_USER")}:{os.environ.get("AUDIOGUILD_POSTGRES_PW")}@{os.environ.get("AUDIOGUILD_DATABASE_URL")}/{os.environ.get("AUDIOGUILD_DATABASE_DB")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True