class Config:

    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Mail configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'magicwebsite03@gmail.com'  # Hardcoded email
    MAIL_PASSWORD = 'zfpuorxboplmcive'  # Hardcoded app password
    MAIL_DEFAULT_SENDER = 'magicwebsite03@gmail.com'  # Hardcoded default sender

    print("MAIL_USERNAME:", MAIL_USERNAME)
    print("MAIL_PASSWORD:", MAIL_PASSWORD)
    print("MAIL_DEFAULT_SENDER:", MAIL_DEFAULT_SENDER)
