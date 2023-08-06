import datetime as dt
import logging
import os
import pandas as pd

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models              import BaseOperator

from ecom_utils.scient.airflow.sql.core.base import GenerateInsertOperator

def execute_pg(query, conn_id):
	status, message = False, ""
	try:
		pg_hook = PostgresHook(postgres_conn_id=conn_id)
		conn = pg_hook.get_conn()
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()
		status=True
		message="Ok"
	except Exception as e:
		logging.error(f"Error ejecutando: {query} - {e}")
		message=str(e)
	finally:
		cur.close()
		conn.close()
	return status, message

def execute_with_conn(conn, query):
	status, message = False, ""
	try:
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()
		status=True
		message="Ok"
	except Exception as e:
		logging.error(f"Error ejecutando consultando: {e}")
		logging.error(f"{query}")
		conn.rollback()
		message=str(e)
	return status, message


def get_conn(conn_id):
	pg_hook = PostgresHook(postgres_conn_id=conn_id)
	conn = pg_hook.get_conn()
	return conn

class PopulatePostgresOperator(BaseOperator):
	template_fields = ["query_file", "errors_file"]

	def __init__(self, query_file, POSTGRES_CONN_ID, errors_file=None, remove_input=True, *args, **kwargs):
		super(PopulatePostgresOperator, self).__init__(*args, **kwargs)
		self.query_file = query_file
		self.POSTGRES_CONN_ID = POSTGRES_CONN_ID

		self.errors_file=errors_file

		self.remove_input=remove_input


	def execute(self, context):
		conn=get_conn(conn_id=self.POSTGRES_CONN_ID)
		
		with open(self.query_file) as sql:
			errores = []
			#  target error_population_instant error_code error_message
			for line in sql:
				clean_query = line.strip()
				if clean_query:
					status, message= execute_with_conn(query=clean_query, conn=conn)# execute_pg(query=clean_query, conn_id=self.POSTGRES_CONN_ID)
					if not status:
						clean_query=clean_query.replace("\'", '+')
						error = {
							"source": "",
							"target": clean_query,
							"error_population_instant": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
							"error_code": "",
							"error_message": message
						}
						errores.append(error)

		if self.errors_file:
			df_errores = pd.DataFrame(errores)
			df_errores.to_csv(self.errors_file, index=False)
		
		# Eliminamos archivos
		if self.remove_input:
			os.remove(self.query_file)

class GenerateInsertPostgresOperator(GenerateInsertOperator):
	pass

class PgQueryToCSV(BaseOperator):
	template_fields = ["output_file"]

	def __init__(self, query, postgres_conn_id, output_file, dtypes=None, *args, **kwargs):
		super(PgQueryToCSV, self).__init__(*args, **kwargs)
		self.query=query
		self.postgres_conn_id=postgres_conn_id
		self.output_file=output_file
		self.dtypes=dtypes

	def execute(self, context):
		pg_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
		conn = pg_hook.get_conn()

		if self.dtypes is None:
			df = pd.read_sql_query(self.query, conn)
		else:
			df = pd.read_sql_query(self.query, conn, dtype=self.dtypes)


		df.to_csv(self.output_file, index=False)
		logging.info(f"Archivo {self.output_file} creado exitosamente!")