import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

def get_connection():
    return psycopg2.connect(os.getenv("SUPABASE_DB_URL"))
