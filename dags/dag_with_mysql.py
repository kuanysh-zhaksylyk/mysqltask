from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.mysql.operators.mysql import MySqlOperator

default_args = {
    "owner": "kuanysh",
    "retries": 5, 
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="mysql_etl_dag",
    default_args=default_args,
    start_date=datetime(2023, 10, 9),
    schedule_interval='@daily'
) as dag:
    task1 = MySqlOperator(
        task_id="mysql_operator",
        mysql_conn_id="mysql_connection",
        sql="""
        CREATE TABLE Staff (
        id INT,
        name VARCHAR(255) NOT NULL,
        position VARCHAR(30),
        birthday Date);
        """
    )
    task1