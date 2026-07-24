from datetime import date

year = int(input('請輸入年份：'))
month = int(input('請輸入月份：'))
day = int(input('請輸入日期：'))

print('這一天是這一年的第{}天'.format(date(year, month, day).timetuple().tm_yday))
