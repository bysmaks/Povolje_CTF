import os

class Config:
    def __init__(self):
        self.pg_ro_url: str = os.getenv('PG_RO_URL')
        self.pg_rw_url: str = os.getenv('PG_RW_URL')
        self.jwt_secret: str = os.getenv('JWT_SECRET')
        self.admin_password: str = os.getenv('ADMIN_PASSWORD')
        self.tg_bot_token: str = os.getenv('TG_BOT_TOKEN')
        self.service_host: str = os.getenv('SERVICE_HOST')
        self.use_https: bool = os.getenv('USE_HTTPS', False)

config = Config()