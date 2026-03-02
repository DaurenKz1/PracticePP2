import re

with open("practice5/raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

#1
price_pattern = "Стоимость\n(.+)"
prices = re.findall(price_pattern, text)
print(prices)

#2
products = re.findall("\d+\.\n(.+)", text)
print(products)

#3
total_amount = re.findall("ИТОГО:\n([\d\s]*,\d{2})", text)
print(total_amount)

#4
datetime_match = re.findall("Время:\s(.+)", text)
print(datetime_match)

#5
payment_match = re.findall("(Банковская карта|Наличные)", text)
print(payment_match)

#6
print("Товары:")
for p in products:
    print("-", p)

print("\nВсе найденные цены:")
for price in prices:
    print("-", price)

print("\nИтого:", total_amount)
print("Дата и время:", datetime_match)
print("Способ оплаты:", payment_match)