from config.config import SUPABASE_KEY, SUPABASE_URL
from supabase import Client, create_client
from typing import Any, Dict
import logging
from pydantic import BaseModel
import time

# * Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# * Definir el modelo de datos
class SupabaseManager:
    def __init__(self):
        url: str = SUPABASE_URL
        key: str = SUPABASE_KEY
        self.client: Client = create_client(url, key)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
try:
    supabase_manager = SupabaseManager()
    logger.info("SupabaseManager instance created successfully")
except Exception as e:
    logger.error(f"Failed to create SupabaseManager instance: {str(e)}")
    supabase_manager = None
