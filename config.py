import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # OpenAI configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Code execution settings
    MAX_EXECUTION_TIME = 10  # seconds
    MAX_OUTPUT_LENGTH = 10000  # characters
    
    # Allowed imports for code execution (security)
    ALLOWED_IMPORTS = {
        'math', 'random', 'datetime', 'json', 'csv', 're', 
        'collections', 'itertools', 'functools', 'operator',
        'numpy', 'pandas', 'matplotlib.pyplot', 'requests'
    } 