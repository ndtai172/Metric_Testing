import itertools
import time
import json
from functions import *
import pandas as pd

time_start = time.time();

##------------EXTRACT-------------------------
products = get_data_from_db('raw_crawled_data/products_data.json')


##------------TRANSFORM-----------------------
unique_products = remove_duplicates(products)                                   #Sàng lọc sản phẩm bị trùng lặp
write_data_to_db(unique_products, 'transformed_data/unique_products_data.json') #và lưu data vào unique_products_data.json

products = get_data_from_db('transformed_data/unique_products_data.json')
for product in products:
    product = format_product_name(product)                                      #Định dạng lại name (xóa các character không hợp lệ)
    product = format_product_price(product)                                     #Định dạng lại price (xóa ký tự đ và dấu '.')
    product = format_product_revenue(product)                                   #Định dạng lại revenue (xóa string thừa và tính toán theo price)

write_data_to_db(products, 'transformed_data/cleaned_products_data.json')       #Lưu data sạch vào cleaned_products_data.json

#------------LOAD-----------------------
data = get_data_from_db('transformed_data/cleaned_products_data.json')
df = pd.DataFrame(data)


df.to_csv('transformed_data/products.csv', index=False, encoding='utf-8')       #Load data vào csv
df.to_excel('transformed_data/products.xlsx', index=False)                      #Load data xlsx

print(time.time() - time_start)
