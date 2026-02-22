def calculate_score(data):
    score = 0

    # =========================
    # 1️⃣ PERFORMANCE (30)
    # =========================

    # Revenue CAGR > 5%
    if data.get("revenue_cagr", 0) > 0.05:
        score += 10

    # Net margin >= 10%
    if data.get("net_margin", 0) >= 0.10:
        score += 10

    # Profit positive (simplified continuous growth)
    if data.get("net_margin", 0) > 0:
        score += 10


    # =========================
    # 2️⃣ RATIOS (30)
    # =========================

    if data.get("pe", 0) and data["pe"] <= 20:
        score += 5

    if data.get("pb", 0) and data["pb"] <= 3:
        score += 5

    if data.get("debt_equity", 0) and data["debt_equity"] <= 1:
        score += 5

    if data.get("roe", 0) >= 0.15:
        score += 10

    if data.get("roa", 0) >= 0.05:
        score += 5


    # =========================
    # 3️⃣ CASH FLOW (40)
    # =========================

    if data.get("fcf_positive", 0):
        score += 15

    if data.get("fcf_growth", 0):
        score += 10

    if data.get("ocf_vs_income", 0):
        score += 10

    if data.get("cf_to_debt", 0) >= 1:
        score += 5

    return score
