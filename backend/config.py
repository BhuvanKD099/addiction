import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "drug_recovery_secret_key_32_bytes_minimum_length_secure_string")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "drug_recovery_jwt_secret_key_32_bytes_minimum_length_secure_string")

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "ai_drug_recovery_system")