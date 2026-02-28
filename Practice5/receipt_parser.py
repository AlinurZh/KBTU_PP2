import re
import json
from datetime import datetime

def parseReceipt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    products = []

    productPattern = r'(\d+)\.\s*\n(.+?)\n([\d,]+)\s*x\s*([\d\s,]+)\n([\d\s,]+)'
    matches = re.finditer(productPattern, text, re.MULTILINE)

    for match in matches:
        product_name = match.group(2).strip()
        quantity = match.group(3).replace(',', '.')
        unit_price = match.group(4).replace(' ', '').replace(',', '.')
        total_price = match.group(5).replace(' ', '').replace(',', '.')

        products.append({
            'name': product_name,
            'quantity': float(quantity),
            'unit_price': float(unit_price),
            'total': float(total_price)
        })

    totalPattern = r'ИТОГО:\s*([\d\s]+,\d{2})'
    totalMatch = re.search(totalPattern, text)
    totalAmount = 0.0
    if totalMatch:
        totalAmount = float(totalMatch.group(1).replace(' ', '').replace(',', '.'))

    datetimePattern = r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})'
    datetimeMatch = re.search(datetimePattern, text)
    receipt_date = None
    receipt_time = None
    if datetimeMatch:
        receipt_date = datetimeMatch.group(1)
        receipt_time = datetimeMatch.group(2)

    paymentPattern = r'(Банковская карта|Наличные|CASH|CARD):'
    paymentMatch = re.search(paymentPattern, text, re.IGNORECASE)
    paymentMethod = paymentMatch.group(1) if paymentMatch else "Не указан"

    companyPattern = r'Филиал\s+(.+)'
    companyMatch = re.search(companyPattern, text)
    companyName = companyMatch.group(1).strip() if companyMatch else None

    binPattern = r'БИН\s+(\d+)'
    binMatch = re.search(binPattern, text)
    binNumber = binMatch.group(1) if binMatch else None

    checkPattern = r'Чек\s+№(\d+)'
    checkMatch = re.search(checkPattern, text)
    checkNumber = checkMatch.group(1) if checkMatch else None

    cashierPattern = r'Кассир\s+(.+)'
    cashierMatch = re.search(cashierPattern, text)
    cashier = cashierMatch.group(1).strip() if cashierMatch else None

    vatPattern = r'в\s+т\.ч\.\s+НДС\s+\d+%:\s*([\d\s]+,\d{2})'
    vatMatch = re.search(vatPattern, text)
    vatAmount = 0.0
    if vatMatch:
        vatAmount = float(vatMatch.group(1).replace(' ', '').replace(',', '.'))

    result = {
        'company': companyName,
        'bin': binNumber,
        'checkNumber': checkNumber,
        'cashier': cashier,
        'date': receipt_date,
        'time': receipt_time,
        'paymentMethod': paymentMethod,
        'products': products,
        'totalItems': len(products),
        'vat': vatAmount,
        'totalAmount': totalAmount
    }

    return result

def printReceiptFormatted(data):
    print("=" * 60)
    print("              ИНФОРМАЦИЯ О ЧЕКЕ")
    print("=" * 60)
    print(f"Компания:        {data['company']}")
    print(f"БИН:             {data['bin']}")
    print(f"Номер чека:      {data['checkNumber']}")
    print(f"Кассир:          {data['cashier']}")
    print(f"Дата:            {data['date']}")
    print(f"Время:           {data['time']}")
    print(f"Способ оплаты:   {data['paymentMethod']}")
    print("=" * 60)
    print(f"{'№':<4} {'Товар':<40} {'Кол-во':<8} {'Цена':<10} {'Сумма':<10}")
    print("-" * 60)

    for i, product in enumerate(data['products'], 1):
        name = product['name'][:37] + "..." if len(product['name']) > 40 else product['name']
        print(f"{i:<4} {name:<40} {product['quantity']:<8.1f} {product['unit_price']:<10.2f} {product['total']:<10.2f}")

    print("=" * 60)
    print(f"{'Всего товаров:':<50} {data['totalItems']}")
    print(f"{'НДС 12%:':<50} {data['vat']:.2f} ₸")
    print(f"{'ИТОГО:':<50} {data['totalAmount']:.2f} ₸")
    print("=" * 60)

def saveToJson(data, outputFile='receiptData.json'):
    with open(outputFile, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nДанные сохранены в {outputFile}")

try:
    receiptData = parseReceipt('raw.txt')
    printReceiptFormatted(receiptData)
    saveToJson(receiptData)

    print("\n" + "=" * 60)
    print("              JSON ФОРМАТ")
    print("=" * 60)
    print(json.dumps(receiptData, ensure_ascii=False, indent=2))

except FileNotFoundError:
    print("Ошибка: файл raw.txt не найден!")
except Exception as e:
    print(f"Ошибка при парсинге: {e}")
    import traceback
    traceback.print_exc()