import pandas as pd
from app.scoring import calculate_fairness_score

def demographic_parity_difference(df, sensitive, target):
    rates = df.groupby(sensitive)[target].mean()
    return float(rates.max() - rates.min())

def demographic_parity_ratio(df, sensitive, target):
    rates = df.groupby(sensitive)[target].mean()
    return float(rates.min() / rates.max()) if rates.max() != 0 else 0.0

def equalized_odds_difference(df, sensitive, target):
    rates = df.groupby(sensitive)[target].mean()
    return float(rates.max() - rates.min())

def interpret_bias(dp_diff):
    if dp_diff < 0.1:
        return "Low Bias"
    elif dp_diff < 0.25:
        return "Moderate Bias"
    else:
        return "High Bias"

def run_fairness_audit(df: pd.DataFrame, sensitive_attr: str, target: str):
    dp_diff = demographic_parity_difference(df, sensitive_attr, target)
    dp_ratio = demographic_parity_ratio(df, sensitive_attr, target)
    eo_diff = equalized_odds_difference(df, sensitive_attr, target)

    score = calculate_fairness_score(dp_diff, dp_ratio, eo_diff)

    return {
        "dataset_size": len(df),
        "sensitive_attribute": sensitive_attr,
        "target_column": target,
        "group_distribution": df[sensitive_attr].value_counts().to_dict(),
        "positive_rate_by_group": df.groupby(sensitive_attr)[target].mean().to_dict(),
        "fairness_metrics": {
            "demographic_parity_difference": round(dp_diff, 3),
            "demographic_parity_ratio": round(dp_ratio, 3),
            "equalized_odds_difference": round(eo_diff, 3)
        },
        "fairness_score": score,
        "bias_interpretation": interpret_bias(dp_diff)
    }
