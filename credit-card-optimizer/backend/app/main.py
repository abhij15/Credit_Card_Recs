from fastapi import FastAPI

from .services.data_generator import generate_transactions


app = FastAPI(title="Credit Card Optimizer API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/generate-data")
async def generate_data():
    """
    Generate synthetic credit card transaction data and save to CSV.
    """
    rows = generate_transactions(
        num_users=500,
        num_transactions=50_000,
        output_path="../../data/raw/transactions.csv",
    )
    return {"status": "success", "rows": rows}


