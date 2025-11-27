import os 

DBHOST = os.getenv('DBHOST', 'postgres')
DBPORT = os.getenv('DBPORT', '5432')
DBNAME = os.getenv('POSTGRES_DB','dbFastApi')
DBUSER = os.getenv('POSTGRES_USER','kcire')
DBPASSWORD = os.getenv('POSTGRES_PASSWORD','123456')

DATABASE_URL = f'postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}'

