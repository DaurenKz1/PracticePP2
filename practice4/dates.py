#1
from datetime import datetime, timedelta

current_date = datetime.now()
new_date = current_date - timedelta(days=5)

print("Current date:", current_date)
print("5 days earlier:", new_date)

#2

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#3

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("With microseconds:", now)
print("Without microseconds:", without_microseconds)

#4

date1 = datetime(2025, 1, 1, 12, 0, 0)
date2 = datetime(2025, 1, 2, 12, 0, 0)

difference = date2 - date1

print("Difference in seconds:", difference.total_seconds())