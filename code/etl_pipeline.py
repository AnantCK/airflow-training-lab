
"""
Agentic ETL Workshop - deterministic ETL core
Run locally or in Google Colab:
    python etl_pipeline.py --data_dir ../data --out_dir ../outputs
"""
import argparse
import json
from pathlib import Path
import pandas as pd

PRODUCT_CORRECTIONS = {
    # AI can suggest mappings, but deterministic code applies only approved mappings.
    "Coffe": "Coffee"
}

def load_inputs(data_dir: Path):
    sales = pd.read_csv(data_dir / "sales_raw.csv")
    product = pd.read_csv(data_dir / "product_master.csv")
    weather = pd.read_json(data_dir / "weather_daily.json")
    return sales, product, weather

def normalize_types(sales: pd.DataFrame) -> pd.DataFrame:
    df = sales.copy()
    df["date_raw"] = df["date"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date.astype("string")
    df["product_raw"] = df["product"]
    df["product"] = df["product"].replace(PRODUCT_CORRECTIONS)
    df["qty_num"] = pd.to_numeric(df["qty"], errors="coerce")
    df["price_num"] = pd.to_numeric(df["price"], errors="coerce")
    return df

def add_quality_flags(df: pd.DataFrame, product_master: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    known_products = set(product_master["product"].tolist())
    out["is_duplicate"] = out.duplicated(subset=["order_id"], keep="first")
    out["invalid_date"] = out["date"].isna()
    out["missing_product"] = out["product"].isna() | (out["product"].astype("string").str.strip() == "")
    out["unknown_product"] = ~out["product"].isin(known_products) & ~out["missing_product"]
    out["missing_qty"] = out["qty_num"].isna()
    out["negative_qty"] = out["qty_num"] < 0
    out["non_numeric_price"] = out["price_num"].isna()
    out["outlier_qty"] = out["qty_num"] > 100
    flag_cols = [
        "is_duplicate", "invalid_date", "missing_product", "unknown_product",
        "missing_qty", "negative_qty", "non_numeric_price", "outlier_qty"
    ]
    out["is_valid"] = ~out[flag_cols].any(axis=1)
    return out

def transform_and_join(flagged: pd.DataFrame, product_master: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:
    valid = flagged[flagged["is_valid"]].copy()
    valid["revenue"] = valid["qty_num"] * valid["price_num"]
    valid = valid.merge(product_master, on="product", how="left")
    weather = weather.copy()
    weather["date"] = pd.to_datetime(weather["date"]).dt.date.astype("string")
    clean = valid.merge(weather, on="date", how="left")
    cols = ["order_id","date","product","qty_num","price_num","channel","category","revenue","temperature_c","rain_mm","condition"]
    clean = clean[cols].rename(columns={"qty_num":"qty", "price_num":"price"})
    return clean

def build_quality_report(flagged: pd.DataFrame) -> dict:
    flag_cols = ["is_duplicate", "invalid_date", "missing_product", "unknown_product", "missing_qty", "negative_qty", "non_numeric_price", "outlier_qty"]
    report = {
        "pipeline": "daily_sales_weather",
        "total_rows": int(len(flagged)),
        "valid_rows": int(flagged["is_valid"].sum()),
        "rejected_rows": int((~flagged["is_valid"]).sum()),
    }
    for col in flag_cols:
        report[col] = int(flagged[col].sum())
    report["severity"] = "HIGH" if report["rejected_rows"] / max(report["total_rows"], 1) > 0.2 else "LOW"
    report["human_review_required"] = report["severity"] == "HIGH" or report["non_numeric_price"] > 0
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data")
    parser.add_argument("--out_dir", default="outputs")
    args = parser.parse_args()
    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sales, products, weather = load_inputs(data_dir)
    normalized = normalize_types(sales)
    flagged = add_quality_flags(normalized, products)
    clean = transform_and_join(flagged, products, weather)
    quality_report = build_quality_report(flagged)

    clean.to_csv(out_dir / "clean_sales_weather.csv", index=False)
    flagged.to_csv(out_dir / "sales_quality_flags.csv", index=False)
    with open(out_dir / "quality_report.json", "w", encoding="utf-8") as f:
        json.dump(quality_report, f, ensure_ascii=False, indent=2)

    print(json.dumps(quality_report, ensure_ascii=False, indent=2))
    print(f"Wrote files to: {out_dir.resolve()}")

if __name__ == "__main__":
    main()
