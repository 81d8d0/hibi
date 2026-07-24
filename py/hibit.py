from datetime import datetime, date

# 讓函數可以接收指定的 datetime 物件
def calculate_day_percentage(target_date=None):
    # 若有傳入指定日期則使用，否則獲取系統當前日期時間
    current_date = target_date if target_date else datetime.now()

    # 獲取年份和一年中的總天數
    year = current_date.year
    total_days_in_year = (datetime(year + 1, 1, 1) - datetime(year, 1, 1)).days

    # 計算指定日期是這一年的第幾天
    day_of_year = (current_date - datetime(year, 1, 1)).days + 1

    # 第幾週
    #week_of_year = current_date.isocalendar()[1]
    # 同時取得 ISO 年份與週數
    iso_year, week_of_year, _ = current_date.isocalendar()

    # 計算已經過了這一年的百分比(浮點數,用於計算長條圖)
    percentage = (day_of_year / total_days_in_year) * 100

    # 格式化百分比字串(用於顯示)
    formatted_percentage = '{:.2f}'.format(percentage).rstrip('0').rstrip('.')

    # 剩幾天
    days_left = total_days_in_year - day_of_year

    # 取得當年最後一週的總週數 (每年 12/28 必然落在該年最後一個 ISO 週)
    total_weeks_in_year = date(year, 12, 28).isocalendar()[1]

    if iso_year < year:
        # 情況：2040-01-01，但 ISO 算在 2039 年第 52 週
        # 此時 iso_year (2039) < year (2040)
        weeks_left = total_weeks_in_year
    elif iso_year > year:
        # 情況：12 月底已經算入明年的第一週
        weeks_left = 0
    else:
        # 一般情況正常相減
        weeks_left = total_weeks_in_year - week_of_year

    # --- 新增:產生長條圖(含四季顏色標記) ---
    bar_length = 60  # 設定長條圖的總長度
    filled_length = int(bar_length * percentage / 100)
    
    # ========== 新增:定義四季分界日與顏色 ==========
    # 計算四季的關鍵日期在一年中的第幾天
    spring_day = (datetime(year, 4, 1) - datetime(year, 1, 1)).days + 1  # 4/1
    summer_day = (datetime(year, 7, 1) - datetime(year, 1, 1)).days + 1  # 7/1
    autumn_day = (datetime(year, 10, 1) - datetime(year, 1, 1)).days + 1  # 10/1
    
    # 將日期轉換為長條圖上的位置
    spring_pos = int(bar_length * spring_day / total_days_in_year)
    summer_pos = int(bar_length * summer_day / total_days_in_year)
    autumn_pos = int(bar_length * autumn_day / total_days_in_year)
    
    # ANSI 顏色代碼
    GREEN = '\033[92m'        # 綠色(春)
    RED = '\033[91m'          # 紅色(夏)
    ORANGE = '\033[38;5;208m' # 橘色(秋)
    RESET = '\033[0m'         # 重置顏色
    
    # 建立長條圖，優先判斷季節位置以保留顏色
    bar = ''
    for i in range(bar_length):
        # 1. 先判斷是否為「季節分界點」，不論過去了沒都要上色
        if i == spring_pos:
            bar += GREEN + '█' + RESET
        elif i == summer_pos:
            bar += RED + '█' + RESET
        elif i == autumn_pos:
            bar += ORANGE + '█' + RESET
        # 2. 如果不是季節分界點，再根據進度決定顯示 █ 或 -
        elif i < filled_length:
            bar += '█'
        else:
            bar += '-'
    # =============================================
    
    progress_bar = f"[{bar}]"

    return day_of_year, week_of_year, days_left, weeks_left, formatted_percentage, progress_bar


# 主程式區塊
if __name__ == "__main__":
    # 1. 取得使用者輸入的測試日期
    user_input = input("請輸入測試日期 (格式 YYYYMMDD，直接 Enter 代表今天): ")
    
    if user_input.strip():
        try:
            # 將字串轉換為 datetime 與 date 物件
            test_datetime = datetime.strptime(user_input, "%Y%m%d")
            start_date = test_datetime.date()
        except ValueError:
            print("⚠️ 格式錯誤！自動切換為系統當前日期。\n")
            test_datetime = datetime.now()
            start_date = date.today()
    else:
        # 直接 Enter 的情況
        test_datetime = datetime.now()
        start_date = date.today()

    # 2. 執行並解構結果 (把測試日期傳進去)
    day_of_year, week_of_year, days_left, weeks_left, percentage_str, bar_display = calculate_day_percentage(test_datetime)

    # 結束日期
    end_date = date(2044, 6, 6)

    # 一年平均上班天數
    workdays_per_year = 250

    # 計算總天數差 (以測試的 start_date 為起點)
    total_days = (end_date - start_date).days

    # 換算成年數(平均一年 365 天)
    years = total_days / 365

    # 估算上班天數
    estimated_workdays = years * workdays_per_year

    # 3. 輸出結果
    print(f"\n【測試基準日: {start_date}】")
    print(f"今日は今年の{day_of_year}日目、第{week_of_year}週です。あと{days_left}日({weeks_left}週)、稼働日は約{estimated_workdays:.0f}日。")
    print(f"{bar_display} {percentage_str}%\n")