## Cài đặt
- Clone file chương trình từ github:
> ```sh
> git clone https://github.com/ndtai172/Metric_Testing
> ```
- Cài đặt các packages sử dụng trong chương trình:
> ```sh
> pip : -r requirements.txt
> ```

## Giải thích cách hoạt động và sử dụng
### Phần 1: Thu thập dữ liệu từ shopee.vn (`testingcrawler/`)
Cấu trúc Tệp và Thư mục:

- `data/products_data.json`: raw data products thu thập được từ shopee (file kết quả).
- `data/sub_categories.json`: data url các sub_categories.
- `functions.py`: chứa các function phục vụ cho chương trình
- `main_crawler.py`: file exec chính kèm commands giải thích cách hoạt động 

![plot](./pics/crawler.png)

### Phần 2: Transform data thu thập được và lưu vào csv, exel (`testing_transformer`)
Cấu trúc Tệp và Thư mục:

- `raw_crawled_data/products_data.json`: raw data products thu thập được từ shopee cho chương trình.
- `transformed_data/unique_products_data.json`: data products đã được lọc duplicate.
- `transformed_data/cleaned_products_data.json`: data products sạch sau khi transform.
- `transformed_data/products.csv` và `transformed_data/products.xlsx`: hai file kết quả.
- `functions.py`: chứa các function phục vụ cho chương trình
- `ETL_run.py`: file exec chính kèm commands giải thích cách hoạt động

![plot](./pics/transformer.png)
 
## Kết quả
- Số sản phẩm dự kiến crawl được: 314*500 = 157000 (dựa vào 27 categories và các sub_categories trong mỗi category, có tổng 314, mỗi sub_categories dự kiến crawl được 500 sản phẩm)
- Số sản phẩm thực tế crawl được: 137996
- Số sản phẩm đã được chuẩn hóa và transform qua csv, exel: 116855
------
- Thời gian crawl (với 9 threads): 8800 seconds
- Thời gian sau ETL và lưu vào csv, exel (với 137996 sản phẩm): 17 second