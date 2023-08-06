import json
import psycopg2
from .base import Connector


class PgConnector(Connector):

    def __init__(self, config_from_local=False, mount_path='/pg-credentials', secret_file='pg.secrets'):
        super().__init__(config_from_local, mount_path, secret_file)

    def _get_client_from_oc(self, mount_path):
        with open(f'{mount_path}/host', 'r') as secret_file:
            host = secret_file.read()
        with open(f'{mount_path}/port', 'r') as secret_file:
            port = secret_file.read()
        with open(f'{mount_path}/database', 'r') as secret_file:
            database = secret_file.read()
        with open(f'{mount_path}/user', 'r') as secret_file:
            user = secret_file.read()
        with open(f'{mount_path}/password', 'r') as secret_file:
            password = secret_file.read()

        return psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
            )

    def _get_client_from_local(self, secret_file):
        with open(secret_file, 'r') as f:
            db_credential = json.load(f)

        return psycopg2.connect(
            host=db_credential['host'],
            port=db_credential['port'],
            database=db_credential['database'],
            user=db_credential['user'],
            password=db_credential['password'])

    def insert_table(self, schema, table, rec):
        cols = list(rec.keys())
        values = [rec[c] for c in cols]
        sql = f"""INSERT INTO {schema}.{table} ({', '.join(cols)}) VALUES ({', '.join(['%s']*len(cols))})"""
        cur = self.client.cursor()
        cur.execute(sql, values)
        self.client.commit()
        cur.close()
        return

    def count_table(self, schema, table):
        cur = self.client.cursor()
        cur.execute(f'select count(*) from {schema}.{table}')
        rec = cur.fetchone()[0]
        cur.close()
        return rec
