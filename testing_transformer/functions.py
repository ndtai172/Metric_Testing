import itertools
import time
import json
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def get_data_from_db(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def write_data_to_db(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def remove_duplicates(products):
    products.sort(key=lambda x: x['product_name'])
    grouped_products = itertools.groupby(products, key=lambda x: x['product_name'])
    unique_products = [next(group) for _, group in grouped_products]
    return unique_products

def format_product_name(product):
    product_name = product["product_name"]

    illegal_chars = ILLEGAL_CHARACTERS_RE.findall(product_name)
    for char in illegal_chars:
        product_name = product_name.replace(char, '')

    product["product_name"] = product_name
    return product

def format_product_price(product):
    product_price = product["product_price"]
    product_price = product_price.replace('₫', '').replace('.', '')

    if product_price == '':
        product["product_price"] = '0'

    product["product_price"] = product_price
    return product


def format_product_revenue(product):
    revenue_str = product["product_revenue"].replace('Đã bán', '').replace(' ', '').replace(',', '.')

    if revenue_str == '':
        product["product_revenue"] = '0'
        return product

    if 'k' in revenue_str:
        revenue_str = revenue_str.replace('k', '')
        sold = float(revenue_str) * 1000
    elif 'tr' in revenue_str:
        revenue_str = revenue_str.replace('tr', '')
        sold = float(revenue_str) * 1000000
    else:
        sold = float(revenue_str)

    if '-' in product["product_price"]:
        prices = product["product_price"].split(' - ')
        formatted_revenue = f"{int(sold) * int(prices[0])} - {int(sold) * int(prices[1])}"
    else:
        formatted_revenue = f"{int(sold) * int(product['product_price'])}"

    product["product_revenue"] = formatted_revenue
    return product


