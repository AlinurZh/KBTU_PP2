from datetime import datetime, timedelta
#1: 
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print(f"Current Date: {current_date.strftime('%Y-%m-%d')}")
print(f"Date 5 days ago: {five_days_ago.strftime('%Y-%m-%d')}")
print()

#2:
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print(f"Yesterday: {yesterday.strftime('%Y-%m-%d')}")
print(f"Today: {today.strftime('%Y-%m-%d')}")
print(f"Tomorrow: {tomorrow.strftime('%Y-%m-%d')}")
print()

#3:
current_datetime = datetime.now()
print(f"With microseconds: {current_datetime}")
without_microseconds = current_datetime.replace(microsecond=0)
print(f"Without microseconds: {without_microseconds}")
print()

#4:
date1 = datetime(2024, 1, 10, 10, 30, 0)
date2 = datetime(2024, 1, 15, 12, 45, 30)
difference_in_seconds = (date2 - date1).total_seconds()
print(f"Date 1: {date1}")
print(f"Date 2: {date2}")
print(f"Difference in seconds: {difference_in_seconds}")