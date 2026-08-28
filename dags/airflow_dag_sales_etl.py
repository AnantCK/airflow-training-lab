
"""
Airflow DAG template for Agentic ETL Workshop.
Place this file in the Airflow dags/ folder.
This DAG calls the deterministic ETL script and stores output files.
"""
from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
import json
import subprocess

from airflow.decorators import dag, task

DEFAULT_ARGS = {
    "owner": "workshop",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

@dag(
    dag_id="agentic_daily_sales_pipeline",
    description="Daily sales ETL with quality report for n8n/AI agent",
    schedule="0 8 * * *",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["etl", "agentic", "workshop","training"],
)
def agentic_daily_sales_pipeline():

    @task
    def run_deterministic_etl() -> str:
        # Adjust paths for your Airflow environment.
        base_dir = Path("/workspaces/airflow-training-lab")
        code_path = base_dir / "code" / "etl_pipeline.py"
        data_dir = base_dir / "data"
        out_dir = base_dir / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "python", str(code_path),
            "--data_dir", str(data_dir),
            "--out_dir", str(out_dir)
        ], check=True)
        return str(out_dir / "quality_report.json")

    @task
    def quality_gate(report_path: str) -> dict:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
        if report.get("human_review_required"):
            # Keep pipeline honest: fail intentionally when review is required.
            raise ValueError(f"Human review required: {json.dumps(report, ensure_ascii=False)}")
        return report

    report_path = run_deterministic_etl()
    quality_gate(report_path)

agentic_daily_sales_pipeline()
