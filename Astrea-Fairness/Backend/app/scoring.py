def calculate_fairness_score(dp_diff, dp_ratio, eo_diff):
    score = 100

    score -= dp_diff * 40
    score -= abs(1 - dp_ratio) * 30
    score -= eo_diff * 30

    return max(0, round(score, 2))
