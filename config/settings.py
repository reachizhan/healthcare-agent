from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    DATABASE_URL:str
    
    OLLAMA_BASE_URL:str
    
    LLM_MODEL:str
    
    EMBEDDING_MODEL: str
    
    RAG_SERVICE_URL: str

    RAG_RETRIEVE_ENDPOINT: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
 
 
    
settings = Settings() # type: ignore