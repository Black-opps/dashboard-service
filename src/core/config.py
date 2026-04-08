from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ANALYTICS_SERVICE_URL: str = "http://mpesa-analytics-api:8000"
    CASHFLOW_SERVICE_URL: str = "http://cashflow-analyzer:8000"
    CATEGORIZER_SERVICE_URL: str = "http://transaction-categorizer:8000"
    PARSER_SERVICE_URL: str = "http://mpesa-transaction-parser:8000"
    TENANT_SERVICE_URL: str = "http://tenant-service:8000"
    AUTH_SERVICE_URL: str = "http://auth-service:8000"

    SERVICE_NAME: str = "dashboard-service"
    SERVICE_PORT: int = 8006
    DEBUG: bool = False

    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
