def calculate_cagr(series):
    """
    คำนวณ CAGR จาก series ที่เรียงจากเก่าสุด -> ใหม่สุด
    """

    # ลบค่า NaN
    series = series.dropna()

    # ต้องมีอย่างน้อย 2 ปี
    if len(series) < 2:
        return 0

    # เรียงเก่าสุด -> ใหม่สุด ให้ชัวร์
    series = series.sort_index()

    start_value = series.iloc[0]      # ปีเก่าสุด
    end_value = series.iloc[-1]       # ปีล่าสุด

    years = len(series) - 1

    # กันค่าศูนย์หรือติดลบ
    if start_value <= 0 or end_value <= 0:
        return 0

    try:
        cagr = (end_value / start_value) ** (1 / years) - 1
        return cagr
    except:
        return 0
