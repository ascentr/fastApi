from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_name: str
    database_username: str
    database_password: str
    secret_key : str
    algorithm : str
    access_token_expires_minutes: int

    database_url = f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'


    class Config:
        env_file = ".env"

settings = Settings()
