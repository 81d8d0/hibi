from datetime import datetime, date

def calculate_day_percentage():
    # 獲取當前日期時間
    current_date = datetime.now()
    
    # 獲取年份和一年中的總天數
    year = current_date.year
    total_days_in_year = (datetime(year + 1, 1, 1) - datetime(year, 1, 1)).days
    
    # 計算今天是這一年的第幾天
    day_of_year = (current_date - datetime(year, 1, 1)).days + 1
    
    # 計算已經過了這一年的百分之多少
    percentage = (day_of_year / total_days_in_year) * 100
    
    # 使用 '{:.2f}'.rstrip('0').rstrip('.') 格式化百分比
    formatted_percentage = '{:.2f}'.format(percentage).rstrip('0').rstrip('.')
    
    # 剩幾天
    if year == 2044:
        # 2044 特例：以 6/4 為倒數終點 (6/3 剩 1 天，1/1 剩 155 天)
        target_date_2044 = date(2044, 6, 4)
        # 算出天數差，並用 max(0, ...) 確保 6/4 之後不會出現負數
        days_left = max(0, (target_date_2044 - current_date.date()).days)
    else:
        # 一般情況：計算距離當年年底的剩餘天數
        days_left = total_days_in_year - day_of_year

    return day_of_year, days_left, formatted_percentage

result = calculate_day_percentage()

print(f"今天是今年的第 {result[0]} 天，剩 {result[1]} 天，已經過了今年的 {result[2]}%")
