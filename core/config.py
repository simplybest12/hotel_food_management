from pydantic_settings import BaseSettings
import urllib.parse

username = urllib.parse.quote_plus('simply_best12')
password = urllib.parse.quote_plus('Deepak@12')
class Settings(BaseSettings):
    project_name: str = "Hotel_Management_Food"
    project_version:str = "1.0.0"
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int
    
    mongo_user: str
    mongo_password: str
    mongo_db: str   
    app_name:str 
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
    @property
    
    def MONGO_URL(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
    

settings = Settings()