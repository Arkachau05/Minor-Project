from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
from app.fairness import run_fairness_audit

app = FastAPI(title="Astrea Dataset Fairness Auditor")

@app.post("/audit-dataset/")
async def audit_dataset(
    file: UploadFile = File(...),
    sensitive_column: str = Form(...),
    target_column: str = Form(...)
):
    df = pd.read_csv(file.file)

    report = run_fairness_audit(
        df=df,
        sensitive_attr=sensitive_column,
        target=target_column
    )

    return report
