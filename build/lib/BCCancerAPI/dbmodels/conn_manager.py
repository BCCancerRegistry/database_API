from sqlalchemy import create_engine
from BCCancerAPI.dbmodels.config import DbConfig


db_url_template = "mssql+pyodbc://{username}:{password}@{hostname}/{dbname}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

rw_url = db_url_template.format(**DbConfig("DB_RW_USER").__dict__)
rw_eng = create_engine(rw_url, pool_size=10, max_overflow=0, echo=True)


def get_rw_eng():
    return rw_eng
