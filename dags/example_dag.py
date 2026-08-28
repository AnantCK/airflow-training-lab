from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="hello_world_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["training"],
) as dag:

    task_hello = BashOperator(
        task_id="print_hello",
        bash_command='echo "ยินดีต้อนรับสู่คอร์สอบรม Airflow!"',
    )