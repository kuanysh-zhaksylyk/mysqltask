from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.mysql.operators.mysql import MySqlOperator

default_args = {
    "owner": "kuanysh",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

dag = DAG('simple-mysql-dag',
          default_args=default_arg,
          schedule_interval='0 0 * * *')

mysql_task = MySqlOperator(dag=dag,
                           mysql_conn_id='mysql_default',
                           task_id='mysql_task',
                           sql='mysql/db_dump_version_2.sql')

mysql_task
