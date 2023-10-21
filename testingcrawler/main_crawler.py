import json
import time
from functions import *

start_time = time.time()

# data = crawl_products('https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567')

##-----Crawl url của 27 category (nhóm hàng) trên trang chủ của shopee------
data_categories = crawl_categories('https://shopee.vn/')
##-----Crawl thêm url của các sub_category có trong mỗi nhóm hàng vừa crawl được và lưu vào data/sub_categories.json------
data_sub_categories = crawl_with_threads(data_categories, 5, crawl_sub_categories, 'data/sub_categories.json')

##-----Crawl các sản phẩm trong từng sub_category-----

json_filename = 'data/sub_categories.json'                                  ##-----Load file chứa url của tất cả sub_category-----
try:
    with open(json_filename, 'r', encoding='utf-8') as json_file:
        sub_categories_data = json.load(json_file)
except Exception:
    pass

i = 0
for item in sub_categories_data:
    urls = generate_urls(item["url"], 9)                                    ## Mỗi sub_category có 9 page từ 1-9,
    crawl_with_threads(urls, 9, crawl_products, 'data/products_data.json')  ## chia làm 9 luồng để khởi động crawl cùng 1 lúc 9 page
    i += 1
    print(f"Da crawl {round(i / len(sub_categories_data) * 100, 2)}%")      ## In ra tiến độ
    # if i==1: break                                                        ## Thêm điều kiện dừng để testing chương trình

print(time.time() - start_time)                                             ## In ra thời gian hoàn thành


