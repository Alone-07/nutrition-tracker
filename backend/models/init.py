from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.engine.url import make_url
from dotenv import load_dotenv
import os

load_dotenv()

db_url = make_url(os.getenv('DATABASE_URL'))

def createDbIfNotExists():
    if not database_exists(db_url):
        create_database(db_url)
        print(f"✅ Database '{db_url.database}' created.")
    else:
        print(f"✅ Database '{db_url.database}' already exists.")
