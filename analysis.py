"""Campaign response analysis for the skin clinic dataset."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent / "skin_clinic_campaign.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Responded"] = (df["Response_to_Campaign"].str.strip().str.lower() == "yes").astype(int)
    df["Product_Category"] = pd.cut(
        df["Unique_Products_Purchased"],
        bins=[0, 4, 8, float("inf")],
        labels=["1-4", "5-8", ">8"],
    )
    return df


def response_table(df: pd.DataFrame, col: str, order: list, label: str) -> pd.DataFrame:
    g = df.groupby(col, observed=True)["Responded"].agg(Customers="count", Responders="sum")
    g = g.reindex(order)
    g["Response Rate (%)"] = (g["Responders"] / g["Customers"] * 100).round(2)
    return g.reset_index().rename(columns={col: label})


def run_analysis(df: pd.DataFrame | None = None) -> dict:
    if df is None:
        df = load_data()
    return {
        "Overall": pd.DataFrame([{
            "Segment": "All customers",
            "Customers": len(df),
            "Responders": int(df["Responded"].sum()),
            "Response Rate (%)": round(df["Responded"].mean() * 100, 2),
        }]),
        "1. Gender vs Campaign Response":
            response_table(df, "Gender", ["Male", "Female"], "Gender"),
        "2. Age Group vs Campaign Response":
            response_table(df, "AgeGroup", ["<30", "30-50", ">50"], "Age Group"),
        "3. Purchase in Last Quarter vs Campaign Response":
            response_table(df, "Purchase_Last_Quarter", ["Yes", "No"], "Purchased Last Quarter"),
        "4. Product Usage vs Campaign Response":
            response_table(df, "Product_Category", ["1-4", "5-8", ">8"], "Unique Products (Last Year)"),
    }


if __name__ == "__main__":
    for name, table in run_analysis().items():
        print(f"\n{name}\n{table.to_string(index=False)}")
