from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    HOST: str = 'localhost'
    PORT: str = 5432
    USER: str = 'postgres'
    PASS: str = 'postgres'
    BASE: str = 'postgres'

    class Config:
        env_file = '.env'
        env_prefix = 'DATABASE_'
        extra = 'allow'


class ServerSettings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    LOG_LEVEL: str = 'info'

    class Config:
        env_file = '.env'
        env_prefix = 'SERVER_'
        extra = 'allow'


class SecuritySettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_ALIVE_IN_DAYS: int = 7
    JWT_REFRESH_TOKEN_ALIVE_IN_DAYS: int = 30

    class Config:
        env_file = '.env'
        env_prefix = 'SECURITY_'
        extra = 'allow'

class DocsSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    SWAGGER_PATH: str = '/swagger'
    REDOC_PATH: str = '/redoc'
    OPENAPI_PATH: str = '/openapi.json'

    class Config:
        env_file = '.env'
        env_prefix = 'DOCS_'
        extra = 'allow'


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    server: ServerSettings = ServerSettings()
    security: SecuritySettings = SecuritySettings()
    docs: DocsSettings = DocsSettings()


settings = Settings()
